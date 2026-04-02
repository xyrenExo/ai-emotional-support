#!/bin/bash

# setup_linode.sh - Initial server preparation for Emotional Support AI

set -e

echo "🛠️ Starting Linode server preparation..."

# Update system
echo "📦 Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "✅ Docker installed."
else
    echo "ℹ️ Docker is already installed."
fi

# Install Docker Compose (V2 is included in newer Docker versions)
echo "🚢 Checking Docker Compose..."
docker compose version || (echo "❌ Docker Compose not found. Please install it manually." && exit 1)

# Install Certbot for SSL
echo "🔒 Installing Certbot..."
sudo apt-get install -y certbot

# Setup UFW Firewall
echo "🛡️ Configuring UFW firewall..."
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

echo "✅ Server preparation complete!"
echo "⚠️ Please log out and log back in for Docker group changes to take effect."
