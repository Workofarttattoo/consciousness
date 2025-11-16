#!/bin/bash
# Reddit API Environment Setup
# Copyright (c) 2025 Joshua Hendricks Cole

echo "🔧 Setting up Reddit API credentials..."
echo ""
echo "Enter your Reddit credentials:"
echo ""

read -p "Reddit Client ID: " REDDIT_CLIENT_ID
read -p "Reddit Client Secret: " REDDIT_CLIENT_SECRET
read -p "Reddit Username: " REDDIT_USERNAME
read -sp "Reddit Password: " REDDIT_PASSWORD
echo ""

# Export for current session
export REDDIT_CLIENT_ID="$REDDIT_CLIENT_ID"
export REDDIT_CLIENT_SECRET="$REDDIT_CLIENT_SECRET"
export REDDIT_USERNAME="$REDDIT_USERNAME"
export REDDIT_PASSWORD="$REDDIT_PASSWORD"
export REDDIT_USER_AGENT="TheGAVL:v1.0 (by /u/$REDDIT_USERNAME)"

# Save to .env file
cat >> /Users/noone/repos/consciousness/.env << ENVEOF

# Reddit API Settings
REDDIT_CLIENT_ID=$REDDIT_CLIENT_ID
REDDIT_CLIENT_SECRET=$REDDIT_CLIENT_SECRET
REDDIT_USERNAME=$REDDIT_USERNAME
REDDIT_PASSWORD=$REDDIT_PASSWORD
REDDIT_USER_AGENT=TheGAVL:v1.0 (by /u/$REDDIT_USERNAME)
ENVEOF

echo ""
echo "✅ Reddit credentials saved!"
echo ""
echo "To activate in current terminal:"
echo "  source setup_reddit_env.sh"
echo ""
echo "To test connection:"
echo "  python3 social_media_automation.py --stats"
