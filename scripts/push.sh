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
echo "🚀 Starting local build and Git push"
echo "=========================================="

# Move to project root (one level above scripts/)
cd "$(dirname "$0")/.."

echo "📦 Building frontend..."
cd frontend
npm run build
cd ..

echo "📂 Staging changes..."
git add .

echo "📝 Creating commit..."
git commit -m "$COMMIT_MESSAGE" || echo "No new changes to commit."

echo "⬆️ Pushing to GitHub..."
git push origin main

echo "=========================================="
echo "✅ Push completed successfully"
echo "=========================================="