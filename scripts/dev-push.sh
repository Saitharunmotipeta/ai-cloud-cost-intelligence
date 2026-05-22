#!/usr/bin/env bash
set -e

echo "=========================================="
echo "🚀 Starting DEV push workflow"
echo "=========================================="

# ------------------------------------------
# Ensure we are on dev branch
# ------------------------------------------

CURRENT_BRANCH=$(git branch --show-current)

if [ "$CURRENT_BRANCH" != "dev" ]; then
  echo "❌ You are not on the dev branch."
  echo "Current branch: $CURRENT_BRANCH"
  exit 1
fi

# ------------------------------------------
# Validate commit message
# ------------------------------------------

if [ -z "$1" ]; then
  echo "❌ Please provide a commit message."
  echo "Example:"
  echo "./scripts/dev-push.sh \"initial commit\""
  exit 1
fi

# ------------------------------------------
# Stage changes
# ------------------------------------------

echo "📂 Staging changes..."
git add .

# ------------------------------------------
# Commit changes
# ------------------------------------------

echo "📝 Creating commit..."
git commit -m "$1"

# ------------------------------------------
# Push to dev branch
# ------------------------------------------

echo "⬆️ Pushing to origin/dev..."
git push origin dev

echo "=========================================="
echo "✅ DEV push completed successfully"
echo "=========================================="