# PyCloudDeployer Tool: README

## Introduction

PyCloudDeployer is an automation tool for managing AWS services, designed to streamline the process of deploying a birthday email system using AWS DynamoDB, Lambda, CloudWatch, SES, IAM, and S3 services.

## System Requirements

- Python 3.7 or later
- AWS CLI
- AWS account with appropriate permissions

## Setup Instructions

### 1. Installing Python

- **Windows:** Download from [Python's official website](https://www.python.org/downloads/), run the installer, and check "Add Python to PATH".
- **macOS/Linux:** Use a package manager (Homebrew for macOS, apt for Linux). Example: `brew install python3`.

### 2. Setting Up a Virtual Environment

- **Creation:**
  - Windows: `python -m venv venv`
  - macOS/Linux: `python3 -m venv venv`
- **Activation:**
  - Windows: `.\venv\Scripts\activate`
  - macOS/Linux: `source venv/bin/activate`
- **Deactivation:** Run `deactivate` in the CLI.

### 3. AWS CLI and Credentials

- Install AWS CLI: [AWS Official Guide](https://aws.amazon.com/cli/).
- Configure AWS CLI: Run `aws configure` and enter your credentials.

### 4. Installing Dependencies with `requirements.txt`

- Ensure `requirements.txt` is present in the root directory.
- Install dependencies:
  - Activate your virtual environment.
  - Run `pip install -r requirements.txt`.

## IAM Setup and Permissions

- The IAM role for this tool requires specific permissions for interacting with various AWS services.
- Permissions include access to DynamoDB, Lambda, CloudWatch, SES, and S3.
- When deploying services, the script will create an IAM role with the necessary permissions.

## Architecture Overview

- **DynamoDB**: Stores user data (emails, names, birthdates).
- **Lambda**: Handles email sending and verification.
- **CloudWatch**: Triggers Lambda functions.
- **SES**: Manages email sending.
- **IAM**: Controls access and permissions.
- **S3**: Optional backup for DynamoDB data.

## Usage and Commands

- **Deploy Services**: `python src/main.py deployservices`
- **Add User**: `python src/main.py adduser`
- **Upload CSV**: `python src/main.py uploadcsv <file_path>`
- **Delete CSV**: `python src/main.py deletecsv <file_path>`
- **Delete User**: `python src/main.py deleteuser`
- **Set Trigger Time**: `python src/main.py settriggertime`
- **Setup SES**: `python src/main.py setupses`
- **Teardown Services**: `python src/main.py teardown`

## Verification and Troubleshooting

- Verify each step via AWS Management Console or CLI output.
- Ensure AWS credentials and configurations are correctly set.
- Confirm Python and dependencies are installed and up to date.
- Troubleshoot issues based on error messages and consult AWS documentation as needed.

## Conclusion

PyCloudDeployer offers a user-friendly approach to managing AWS services for automated email functionalities. Its integration with AWS services and Python-based CLI makes it a convenient tool for users with basic AWS and Python knowledge.
