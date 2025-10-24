#!/bin/bash

# Script simple para crear el paquete de despliegue
# Uso: ./simple-deploy.sh

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

print_status "🚀 Creating deployment package for AWS EC2..."

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
    config.py

print_success "✅ Deployment package created: lab-05-deployment.tar.gz"

echo ""
echo "📦 Package contents:"
tar -tzf lab-05-deployment.tar.gz | head -20
echo "..."

echo ""
echo "🌐 Next steps:"
echo "1. Upload the package to your EC2 instance:"
echo "   scp -i ~/Downloads/laboratorio-05.pem lab-05-deployment.tar.gz ec2-user@YOUR_EC2_IP:/home/ec2-user/"
echo ""
echo "2. Connect to your EC2 instance:"
echo "   ssh -i ~/Downloads/laboratorio-05.pem ec2-user@YOUR_EC2_IP"
echo ""
echo "3. Extract and deploy:"
echo "   cd /home/ec2-user"
echo "   tar -xzf lab-05-deployment.tar.gz"
echo "   cd lab-05"
echo "   chmod +x deploy-aws.sh"
echo "   ./deploy-aws.sh"
echo ""
echo "4. Access your application:"
echo "   http://YOUR_EC2_IP/profesores/"
echo ""
echo "🔍 To get your EC2 public IP, check the AWS Console or run:"
echo "   aws ec2 describe-instances --query 'Reservations[*].Instances[*].PublicIpAddress' --output text"
echo ""

print_success "🎉 Ready for deployment!"
