# Cloud Project Setup Guide

## Prerequisites

Before starting the project, ensure you have the following tools installed:

### Required Software
1. **Python 3.9+**
    ```bash
    # Check Python version
    python3 --version
    ```

2. **Docker**
    ```bash
    # Check Docker version
    docker --version
    ```

3. **AWS CLI**
    ```bash
    # Install AWS CLI
    pip install awscli
    
    # Configure AWS CLI
    aws configure
    ```

4. **LocalStack**
    ```bash
    # Install LocalStack
    pip install localstack
    
    # Start LocalStack
    localstack start
    ```

5. **Terraform**
    ```bash
    # Install Terraform (Ubuntu/Debian)
    curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
    sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
    sudo apt-get update && sudo apt-get install terraform

    # For arch
    yay -S terraform
    ```

### Python Dependencies
Create a virtual environment and install required packages:
```bash
python3 -m venv venv
source venv/bin/activate
pip install boto3
```

## Project Structure
```
.
├── main.tf
├── lambda/
│   └── lambda_function.py
│   └── requirements.txt
├── tests/
│   └── test1.sh
├── update_lambda.sh
├── requirements.txt
└── README.md
```

## Environment Setup
1. Clone the repository
2. Create and activate virtual environment
3. Install dependencies
4. Start LocalStack
5. Initialize Terraform

## Next Steps
- Configure AWS credentials
- Set up local development environment
- Run initial infrastructure tests

Note: Make sure all services are running and properly configured before starting development.