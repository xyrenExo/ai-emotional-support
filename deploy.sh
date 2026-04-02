#!/bin/bash

# Emotional Support AI - Deployment Script for Linode
# Usage: ./deploy.sh [your-domain.com] [your-email@example.com]

set -e

DOMAIN=${1:-$DOMAIN}
EMAIL=${2:-$EMAIL}

if [ -z "$DOMAIN" ]; then
    echo "❌ Error: Domain not provided. Usage: ./deploy.sh [your-domain.com] [your-email@example.com]"
    exit 1
fi

echo "🚀 Starting deployment of Emotional Support AI for $DOMAIN..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Pull latest changes
echo "📦 Pulling latest code..."
git pull origin main || echo "⚠️ Git pull failed. Continuing with local files..."

# Ensure SSL directory exists
mkdir -p ./ssl

# Build and start Docker containers
echo "🐳 Building Docker images..."
docker-compose build

echo "🚢 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready (30s)..."
sleep 30

# Run database migrations
echo "🗄️ Running database migrations..."
docker-compose exec backend python -c "from app import create_app; from app.models import db; db.create_all()" || echo "⚠️ Migrations failed."

# Setup SSL with Certbot (if not already handled by a real cert)
if [ ! -f ./ssl/cert.pem ] && [ "$DOMAIN" != "localhost" ]; then
    echo "🔒 Setting up SSL certificate for $DOMAIN..."
    sudo certbot certonly --standalone -d "$DOMAIN" --email "$EMAIL" --agree-tos --non-interactive
    sudo cp "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ./ssl/cert.pem
    sudo cp "/etc/letsencrypt/live/$DOMAIN/privkey.pem" ./ssl/key.pem
    sudo chown $USER:$USER ./ssl/*.pem
    docker-compose restart nginx
fi

# Check health
echo "🏥 Checking service health..."
curl -f "http://localhost:5000/api/health" || echo "⚠️ Health check failed. Check logs with 'docker-compose logs backend'"

echo "✅ Deployment complete!"
echo "🌐 Application is running at https://$DOMAIN"
echo "📊 Monitor logs with: docker-compose logs -f"