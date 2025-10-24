#!/bin/bash

# Script para transferir archivos a AWS EC2
# Uso: ./transfer-to-aws.sh YOUR_PUBLIC_IP YOUR_KEY.pem

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check arguments
if [ $# -ne 2 ]; then
    print_error "Usage: $0 <PUBLIC_IP> <KEY_FILE>"
    echo "Example: $0 54.123.45.67 my-key.pem"
    exit 1
fi

PUBLIC_IP=$1
KEY_FILE=$2

# Check if key file exists
if [ ! -f "$KEY_FILE" ]; then
    print_error "Key file $KEY_FILE not found"
    exit 1
fi

print_status "Preparing files for AWS EC2 deployment..."

# Create deployment package
print_status "Creating deployment package..."
tar -czf lab-05-deployment.tar.gz \
    app/ \
    dockerfile \
    docker-compose.aws.yml \
    requirements.txt \
    database.sql \
    deploy-aws.sh \
    env.aws \
    run.py \
    config.py \
    run_production.py

print_success "Deployment package created: lab-05-deployment.tar.gz"

# Transfer files to EC2
print_status "Transferring files to EC2 instance $PUBLIC_IP..."
scp -i "$KEY_FILE" lab-05-deployment.tar.gz ec2-user@$PUBLIC_IP:/home/ec2-user/

if [ $? -eq 0 ]; then
    print_success "Files transferred successfully!"
    
    echo ""
    echo "Next steps:"
    echo "1. Connect to your EC2 instance:"
    echo "   ssh -i $KEY_FILE ec2-user@$PUBLIC_IP"
    echo ""
    echo "2. Extract and deploy:"
    echo "   cd /home/ec2-user"
    echo "   tar -xzf lab-05-deployment.tar.gz"
    echo "   cd lab-05"
    echo "   chmod +x deploy-aws.sh"
    echo "   ./deploy-aws.sh"
    echo ""
    echo "3. Access your application:"
    echo "   http://$PUBLIC_IP/profesores/"
    echo ""
else
    print_error "Failed to transfer files"
    exit 1
fi
