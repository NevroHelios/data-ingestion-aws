# CSV Processing System with AWS and Terraform

This project implements a serverless CSV processing system using AWS services and Terraform for infrastructure as code. The system processes CSV files uploaded to S3, extracts metadata, and stores it in DynamoDB.

## Demo
[](./demo/demo.mp4)

## Architecture Overview

The system consists of the following components:

1. **S3 Bucket**: Stores uploaded CSV files
2. **Lambda Function**: Processes CSV files when uploaded
3. **DynamoDB Table**: Stores metadata about processed CSV files
4. **IAM Roles and Policies**: Manages permissions between services

## Tech Stack

- **AWS Services**: S3, Lambda, DynamoDB, IAM
- **Infrastructure**: Terraform
- **Runtime**: Python 3.9
- **Local Development**: LocalStack
- **Testing**: AWS CLI

## How It Works

1. Users upload CSV files to the S3 bucket
2. S3 triggers the Lambda function when a CSV file is created
3. The Lambda function:
   - Reads the CSV data
   - Extracts metadata (columns, row count, etc.)
   - Validates data consistency
   - Stores results in DynamoDB
4. Metadata is retrievable from DynamoDB for analysis

## Prerequisites

- Terraform >= 1.0
- AWS CLI
- Docker (for LocalStack)
- Python 3.9 (for Lambda development)

## Setup and Installation

1. Clone the repository

2. Start LocalStack:
   ```bash
   docker run -d -p 4566:4566 -p 4571:4571 localstack/localstack
   ```
   or
   ```bash
   localstack start
   ```

3. Initialize Terraform:
   ```bash
   terraform init
   ```

4. Apply Terraform configuration:
   ```bash
   terraform apply --auto-approve
   ```

## Configuration Details

### S3 Bucket (`csv-processing-bucket`)
- Configured with a 10MB file size limit for uploads

### DynamoDB Table (`csv_metadata`)
- Primary key: `id` (Lambda request ID)
- Global Secondary Index: `FilenameIndex` for querying by filename

### Lambda Function (`csv_processor`)
- Runtime: Python 3.9
- Timeout: 30 seconds
- Environment Variables:
  - `DYNAMODB_TABLE`: Name of the metadata DynamoDB table

## Testing

Run the test script which uploads a sample CSV file and checks the DynamoDB table:

```bash
./tests/test1.sh
```

This script:
1. Uploads the sample Housing.csv file to the S3 bucket
2. Scans the DynamoDB table to verify metadata has been stored

## Updating the Lambda Function

If you make changes to the Lambda code, use the provided update script:

```bash
./update_lambda.sh
```

This script:
1. Installs dependencies from requirements.txt
2. Creates a new ZIP package
3. Updates the Lambda function with the new code

## Data Structure

The Housing.csv dataset contains real estate information with the following columns:
- price
- area
- bedrooms
- bathrooms
- stories
- mainroad
- guestroom
- basement
- hotwaterheating
- airconditioning
- parking
- prefarea
- furnishingstatus

## Metadata Storage

For each processed CSV file, the Lambda function stores the following metadata:
- File ID (request ID)
- Filename
- Upload timestamp
- File size in bytes
- Row count
- Column count
- Column names
- Count of inconsistent rows
- Processing status

## File Size Limits

The S3 bucket policy restricts uploads to 10MB maximum file size to prevent processing very large files.

## Local Development

The project uses LocalStack to simulate AWS services locally, with endpoints configured in main.tf.