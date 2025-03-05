import os
import json
import sys
import boto3
from datetime import datetime
import io
import csv

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def lambda_handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        response = s3.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        
        csv_reader = csv.reader(io.StringIO(file_content))
        headers = next(csv_reader)  
        rows = list(csv_reader)   
        
        metadata = {
            'id': context.aws_request_id,
            'filename': key,
            'upload_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'file_size_bytes': response['ContentLength'],
            'row_count': len(rows),
            'column_count': len(headers),
            'column_names': headers
        }
        
        table.put_item(Item=metadata)
        
        return {
            'statusCode': 200,
            'body': json.dumps(metadata)
        }
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise e
