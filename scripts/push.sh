#!/usr/bin/env bash
set -e

# -----------------------------------------
# Usage:
# ./scripts/push.sh "Your commit message"
# -----------------------------------------

if [ -z "$1" ]; then
    echo "Usage: ./scripts/push.sh \"Your commit message\""
    exit 1
fi

COMMIT_MESSAGE="$1"

echo "=========================================="
echo "🚀 AI Cloud Cost Intelligence"
echo "Local Validation & Git Push"
echo "=========================================="

# --------------------------------------------------
# Move to Project Root
# --------------------------------------------------

cd "$(dirname "$0")/.."

# --------------------------------------------------
# Pull Latest Changes
# --------------------------------------------------

echo ""
echo "📥 Pulling latest changes..."

git pull origin main

# --------------------------------------------------
# Build Frontend
# --------------------------------------------------

echo ""
echo "📦 Building Frontend..."

cd frontend

npm install
npm run build

cd ..

echo "✅ Frontend build successful."

# --------------------------------------------------
# Build Backend
# --------------------------------------------------

echo ""
echo "🐳 Building Backend Docker Images..."

cd infrastructure/docker

docker-compose build

echo "✅ Backend Docker build successful."

cd ../..

# --------------------------------------------------
# Git Operations
# --------------------------------------------------

echo ""
echo "📂 Staging changes..."

git add .

echo ""
echo "📝 Creating commit..."

git commit -m "$COMMIT_MESSAGE" || echo "No new changes to commit."

echo ""
echo "⬆️ Pushing to GitHub..."

git push origin main

echo ""
echo "=========================================="
echo "✅ Local Validation Successful"
echo "🚀 Code pushed to GitHub"
echo "=========================================="