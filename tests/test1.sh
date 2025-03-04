# uploading csv
aws s3 cp data/Housing.csv s3://csv-processing-bucket/ --endpoint-url http://localhost:4566

# verify dynamoDB entry
aws dynamodb scan --table-name csv_metadata --endpoint-url http://localhost:4566
