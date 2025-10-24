#!/bin/bash

# Deployment script for Flask application
# This script builds and runs the Docker containers

echo "🚀 Starting deployment of Flask Professor Management System..."

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start containers
echo "🔨 Building and starting containers..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

# Test the application
echo "🧪 Testing application..."
if curl -f http://localhost:5001/profesores/api > /dev/null 2>&1; then
    echo "✅ Application is running successfully!"
    echo "🌐 Access the application at: http://localhost:5001/profesores/"
    echo "📊 API endpoint: http://localhost:5001/profesores/api"
else
    echo "❌ Application failed to start. Check logs with: docker-compose logs"
fi

echo "📋 Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop services: docker-compose down"
echo "  - Restart services: docker-compose restart"
echo "  - View running containers: docker-compose ps"
