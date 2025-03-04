# lambda/lambda_function.py
import os
import json
import boto3
import pandas as pd
from datetime import datetime
import io

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def lambda_handler(event, context):
    try:
        # Extract bucket and key from event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        # Get CSV file from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read()
        
        # Process CSV
        df = pd.read_csv(io.BytesIO(file_content))
        
        # Extract metadata
        metadata = {
            'id': context.aws_request_id,
            'filename': key,
            'upload_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'file_size_bytes': response['ContentLength'],
            'row_count': len(df),
            'column_count': len(df.columns),
            'column_names': list(df.columns)
        }
        
        # Store in DynamoDB
        table.put_item(Item=metadata)
        
        return {
            'statusCode': 200,
            'body': json.dumps(metadata)
        }
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise e
