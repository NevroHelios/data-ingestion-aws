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
        # Validate event structure
        if not event.get('Records') or len(event['Records']) == 0:
            print("Error: Invalid event structure - missing Records")
            raise ValueError("Invalid event structure: missing Records")
        
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        print(f"Processing file: s3://{bucket}/{key}")
        
        try:
            response = s3.get_object(Bucket=bucket, Key=key)
        except s3.exceptions.NoSuchKey:
            print(f"Error: File does not exist: s3://{bucket}/{key}")
            raise
            
        file_content = response['Body'].read().decode('utf-8')
        
        if not file_content.strip():
            print("Warning: File is empty or contains only whitespace")
            metadata = {
                'id': context.aws_request_id,
                'filename': key,
                'upload_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'file_size_bytes': 0,
                'row_count': 0,
                'column_count': 0,
                'column_names': [],
                'status': 'empty_file'
            }
            table.put_item(Item=metadata)
            return {
                'statusCode': 200,
                'body': json.dumps(metadata)
            }
        
        try:
            csv_reader = csv.reader(io.StringIO(file_content))
            headers = next(csv_reader, [])
            
            if not headers:
                print("Warning: CSV file has no headers")
            
            rows = list(csv_reader)
            
            inconsistent_rows = 0
            for i, row in enumerate(rows):
                if len(row) != len(headers):
                    inconsistent_rows += 1
                    if inconsistent_rows <= 3:  # Limit logging
                        print(f"Warning: Row {i+1} has {len(row)} columns, expected {len(headers)}")
            
            if inconsistent_rows > 0:
                print(f"Found {inconsistent_rows} rows with inconsistent column counts")
        except csv.Error as csv_err:
            print(f"Error parsing CSV: {str(csv_err)}")
            raise
        
        metadata = {
            'id': context.aws_request_id,
            'filename': key,
            'upload_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'file_size_bytes': response['ContentLength'],
            'row_count': len(rows),
            'column_count': len(headers),
            'column_names': headers,
            'inconsistent_rows': inconsistent_rows,
            'status': 'success'
        }
        
        table.put_item(Item=metadata)
        
        return {
            'statusCode': 200,
            'body': json.dumps(metadata)
        }
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        try:
            error_metadata = {
                'id': context.aws_request_id,
                'error_message': str(e),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'error'
            }
            table.put_item(Item=error_metadata)
        except:
            print("Failed to record error in DynamoDB")
        raise e
