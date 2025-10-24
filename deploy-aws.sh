#!/bin/bash

# AWS EC2 Deployment Script for Flask Professor Management System
# This script deploys the application on AWS EC2 with Docker

set -e  # Exit on any error

echo "🚀 Starting AWS EC2 deployment of Flask Professor Management System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root for security reasons"
   exit 1
fi

# Update system packages
print_status "Updating system packages..."
sudo yum update -y

# Install Docker
print_status "Installing Docker..."
if ! command -v docker &> /dev/null; then
    sudo yum install -y docker
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -a -G docker $USER
    print_success "Docker installed successfully"
else
    print_warning "Docker is already installed"
fi

# Install Docker Compose
print_status "Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
    print_success "Docker Compose installed successfully"
else
    print_warning "Docker Compose is already installed"
fi

# Install additional tools
print_status "Installing additional tools..."
sudo yum install -y curl wget git

# Create application directory
APP_DIR="/home/ec2-user/lab-05"
print_status "Setting up application directory: $APP_DIR"

if [ ! -d "$APP_DIR" ]; then
    mkdir -p $APP_DIR
    print_success "Application directory created"
else
    print_warning "Application directory already exists"
fi

# Copy application files (this would be done via git clone or scp)
print_status "Application files should be copied to $APP_DIR"
print_warning "Please ensure all application files are in $APP_DIR before continuing"

# Set up environment file
print_status "Setting up environment configuration..."
if [ -f "$APP_DIR/env.aws" ]; then
    cp $APP_DIR/env.aws $APP_DIR/.env
    print_success "Environment file configured"
else
    print_error "Environment file (env.aws) not found in $APP_DIR"
    exit 1
fi

# Navigate to application directory
cd $APP_DIR

# Stop existing containers
print_status "Stopping existing containers..."
docker-compose -f docker-compose.aws.yml down || true

# Build and start containers
print_status "Building and starting containers..."
docker-compose -f docker-compose.aws.yml up --build -d

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 60

# Check if services are running
print_status "Checking service status..."
docker-compose -f docker-compose.aws.yml ps

# Get instance public IP
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
print_success "Instance public IP: $PUBLIC_IP"

# Test the application
print_status "Testing application..."
sleep 10
if curl -f http://localhost/profesores/api > /dev/null 2>&1; then
    print_success "Application is running successfully!"
    echo ""
    echo "🌐 Access the application at:"
    echo "   Web Interface: http://$PUBLIC_IP/profesores/"
    echo "   API Endpoint: http://$PUBLIC_IP/profesores/api"
    echo ""
    echo "📊 Database Information:"
    echo "   Host: $PUBLIC_IP"
    echo "   Port: 3306"
    echo "   Database: lab_05"
    echo "   User: flask_user"
    echo ""
else
    print_error "Application failed to start. Checking logs..."
    docker-compose -f docker-compose.aws.yml logs flask_app
    exit 1
fi

# Configure firewall (if needed)
print_status "Configuring firewall..."
sudo firewall-cmd --permanent --add-port=80/tcp || true
sudo firewall-cmd --permanent --add-port=3306/tcp || true
sudo firewall-cmd --reload || true

print_success "Deployment completed successfully!"
echo ""
echo "📋 Useful commands:"
echo "  - View logs: docker-compose -f docker-compose.aws.yml logs -f"
echo "  - Stop services: docker-compose -f docker-compose.aws.yml down"
echo "  - Restart services: docker-compose -f docker-compose.aws.yml restart"
echo "  - View running containers: docker-compose -f docker-compose.aws.yml ps"
echo "  - Update application: git pull && docker-compose -f docker-compose.aws.yml up --build -d"
echo ""
echo "🔒 Security Notes:"
echo "  - Change default passwords in production"
echo "  - Configure AWS Security Groups properly"
echo "  - Enable SSL/TLS for production use"
echo "  - Regular security updates recommended"
