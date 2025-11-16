#!/bin/bash
# ECH0 Environment Setup
# Copyright (c) 2025 Joshua Hendricks Cole

export EMAIL_ADDRESS='inventor@aios.is'
export CALENDLY_API_KEY='eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNzYxNzIyNzk4LCJqdGkiOiI1MDBhMWQxNy1hMTllLTQxMzYtYjgwMS1kZmY3MmM3NmUyNzUiLCJ1c2VyX3V1aWQiOiI1NDA1YmJiOC1kMWI2LTRiYzAtOGU4Ni04YTQ0ZDkxOGY2YTcifQ.nbxtTq6WfhMC1xWKmCGggieFbr3cc4lDm72VCY2zq02KCJegtBP4HRrLnG_nBjzAsnVU8Q5ZFo5lfS2imYL6xQ'

echo "✅ Calendly API key set"
echo "🔍 Fetching your Calendly User URI..."

# Get user URI from Calendly API
USER_URI=$(curl -s --request GET \
  --url 'https://api.calendly.com/users/me' \
  --header "Authorization: Bearer $CALENDLY_API_KEY" \
  --header 'Content-Type: application/json' | python3 -c "import sys, json; print(json.load(sys.stdin)['resource']['uri'])" 2>/dev/null)

if [ -n "$USER_URI" ]; then
    export CALENDLY_USER_URI="$USER_URI"
    echo "✅ Calendly User URI: $USER_URI"
else
    echo "❌ Failed to fetch User URI"
    exit 1
fi

echo ""
echo "✅ ECH0 environment configured!"
echo ""
echo "To activate, run:"
echo "  source setup_ech0_env.sh"
