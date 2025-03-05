# lambda/lambda_function.py
import os
import json
import sys
import boto3
from datetime import datetime
import io
import csv

# Debug information
print(f"Python version: {sys.version}")
print(f"PYTHONPATH: {sys.path}")
print(f"Current directory contents: {os.listdir('.')}")
print(f"Layer directory contents: {os.listdir('/opt') if os.path.exists('/opt') else 'No /opt directory'}")
print(f"Layer python directory contents: {os.listdir('/opt/python') if os.path.exists('/opt/python') else 'No /opt/python directory'}")

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
        file_content = response['Body'].read().decode('utf-8')
        
        # Process CSV
        csv_reader = csv.reader(io.StringIO(file_content))
        headers = next(csv_reader)  # Get column names
        rows = list(csv_reader)     # Get all rows
        
        # Extract metadata
        metadata = {
            'id': context.aws_request_id,
            'filename': key,
            'upload_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'file_size_bytes': response['ContentLength'],
            'row_count': len(rows),
            'column_count': len(headers),
            'column_names': headers
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
