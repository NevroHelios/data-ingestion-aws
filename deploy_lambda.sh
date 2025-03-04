#!/bin/bash

# Create a temporary directory for building the package
mkdir -p lambda_build
cd lambda_build

# Copy the Lambda function code
cp ../lambda/lambda_function.py .
cp ../lambda/requirements.txt .

# Install dependencies directly into the package directory
pip install -r requirements.txt -t .

# Create the zip package
zip -r ../lambda.zip .

# Clean up
cd ..
rm -rf lambda_build

echo "Lambda package created successfully."3