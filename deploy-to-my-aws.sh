#!/bin/bash

# Script para desplegar en AWS EC2 con la clave laboratorio-05.pem
# Uso: ./deploy-to-my-aws.sh YOUR_PUBLIC_IP

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
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

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check arguments
if [ $# -ne 1 ]; then
    print_error "Usage: $0 <PUBLIC_IP>"
    echo "Example: $0 54.123.45.67"
    echo ""
    echo "To get your EC2 public IP, run:"
    echo "aws ec2 describe-instances --query 'Reservations[*].Instances[*].PublicIpAddress' --output text"
    exit 1
fi

PUBLIC_IP=$1
KEY_FILE="$HOME/Downloads/laboratorio-05.pem"

# Check if key file exists
if [ ! -f "$KEY_FILE" ]; then
    print_error "Key file $KEY_FILE not found"
    exit 1
fi

print_status "🚀 Starting deployment to AWS EC2 instance: $PUBLIC_IP"

# Test connection first
print_status "Testing SSH connection..."
if ssh -i "$KEY_FILE" -o ConnectTimeout=10 -o StrictHostKeyChecking=no ec2-user@$PUBLIC_IP "echo 'Connection successful'" > /dev/null 2>&1; then
    print_success "SSH connection successful"
else
    print_error "Cannot connect to EC2 instance. Please check:"
    echo "  - Public IP address is correct: $PUBLIC_IP"
    echo "  - Security Group allows SSH (port 22)"
    echo "  - Instance is running"
    exit 1
fi

# Transfer files
print_status "Transferring deployment package to EC2..."
scp -i "$KEY_FILE" lab-05-deployment.tar.gz ec2-user@$PUBLIC_IP:/home/ec2-user/

if [ $? -eq 0 ]; then
    print_success "Files transferred successfully!"
else
    print_error "Failed to transfer files"
    exit 1
fi

# Execute deployment on EC2
print_status "Executing deployment on EC2..."
ssh -i "$KEY_FILE" ec2-user@$PUBLIC_IP << 'EOF'
    set -e
    
    echo "📦 Extracting deployment package..."
    cd /home/ec2-user
    tar -xzf lab-05-deployment.tar.gz
    cd lab-05
    
    echo "🔧 Making deployment script executable..."
    chmod +x deploy-aws.sh
    
    echo "🚀 Starting deployment..."
    ./deploy-aws.sh
EOF

if [ $? -eq 0 ]; then
    print_success "🎉 Deployment completed successfully!"
    echo ""
    echo "🌐 Your application is now available at:"
    echo "   Web Interface: http://$PUBLIC_IP/profesores/"
    echo "   API Endpoint: http://$PUBLIC_IP/profesores/api"
    echo ""
    echo "📊 Database Information:"
    echo "   Host: $PUBLIC_IP"
    echo "   Port: 3306"
    echo "   Database: lab_05"
    echo "   User: flask_user"
    echo ""
    echo "🔍 To monitor your application:"
    echo "   ssh -i $KEY_FILE ec2-user@$PUBLIC_IP"
    echo "   cd /home/ec2-user/lab-05"
    echo "   docker-compose -f docker-compose.aws.yml ps"
    echo "   docker-compose -f docker-compose.aws.yml logs -f"
else
    print_error "Deployment failed. Please check the logs above."
    exit 1
fi
