#!/bin/bash

pip install -r lambda/requirements.txt -t lambda
cd lambda
zip -r ../lambda.zip .
cd ..
aws lambda update-function-code \
  --function-name csv_processor \
  --zip-file fileb://lambda.zip \
  --region us-east-1 \
  --endpoint-url http://localhost:4566