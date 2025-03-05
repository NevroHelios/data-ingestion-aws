aws s3 cp data/Housing.csv s3://csv-processing-bucket/ --endpoint-url http://localhost:4566 && aws dynamodb scan --table-name csv_metadata --endpoint-url http://localhost:4566
