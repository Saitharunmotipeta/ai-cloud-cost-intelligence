#!/usr/bin/env bash
set -e

# ==========================================
# deploy.sh
#
# Deploys frontend and backend to AWS.
#
# What it does:
# 1. Uploads frontend/dist to S3
# 2. Invalidates CloudFront cache
# 3. SSH into EC2
# 4. Pulls latest code from GitHub
# 5. Rebuilds and restarts Docker containers
#
# Usage:
# ./scripts/deploy.sh
# ==========================================

# ------------------------------------------
# Move to project root
# ------------------------------------------

cd "$(dirname "$0")/.."

source .env

echo "=========================================="
echo "🚀 Starting AWS deployment"
echo "=========================================="

# ------------------------------------------
# Step 1: Verify frontend build exists
# ------------------------------------------

if [ ! -d "frontend/dist" ]; then
  echo "❌ frontend/dist not found."
  echo "Run npm run build first or use push.sh."
  exit 1
fi

# ------------------------------------------
# Step 2: Upload frontend to S3
# ------------------------------------------

echo "📦 Uploading frontend build to S3..."
aws s3 sync frontend/dist/ "s3://$S3_BUCKET" --delete

# ------------------------------------------
# Step 3: Invalidate CloudFront cache
# ------------------------------------------

echo "🌐 Creating CloudFront invalidation..."
aws cloudfront create-invalidation \
  --distribution-id "$CLOUDFRONT_DISTRIBUTION_ID" \
  --paths "/*"

# ------------------------------------------
# Step 4: Deploy backend on EC2
# ------------------------------------------

echo "🖥️ Connecting to EC2 and updating services..."
echo $REMOTE_PROJECT_DIR

ssh -i "$SSH_KEY_PATH" "$EC2_HOST" << EOF
set -e

echo "📂 Switching to project directory..."
cd $REMOTE_PROJECT_DIR



echo "⬇️ Pulling latest code..."
git pull origin main

echo "🐳 Switching to Docker directory..."
cd infrastructure/docker

echo "🐳 Rebuilding and restarting containers..."
docker-compose up -d --build

echo "📊 Running containers:"
docker-compose ps
EOF

# ------------------------------------------
# Completed
# ------------------------------------------

echo "=========================================="
echo "✅ Deployment completed successfully"
echo "=========================================="