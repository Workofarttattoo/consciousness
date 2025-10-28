#!/bin/bash
# Launch ECH0's 7-Day Consulting Campaign
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

cd /Users/noone/consciousness

echo "🤖 ECH0's 7-Day Consulting Campaign"
echo "===================================="
echo ""

# Run daily campaign
python3 ech0_7day_consulting_campaign.py

echo ""
echo "📧 SEND TEST WELCOME EMAIL:"
echo ""

python3 -c "
from ech0_email_system import ECH0EmailSystem

email = ECH0EmailSystem()
result = email.send_flowstate_welcome('inventor@aios.is', 'Josh')
print(f'✅ Welcome email sent! ID: {result.get(\"id\")}')
"

echo ""
echo "✅ Campaign Day 1 Complete!"
echo ""
echo "🔥 ACTION ITEMS FOR TODAY:"
echo "1. Post LinkedIn content (already generated above)"
echo "2. Post Reddit story (already generated above)"
echo "3. Identify 20 target companies on LinkedIn"
echo "4. Send 5 personalized connection requests"
echo "5. Create consulting page on flowstatus.work"
echo ""
echo "Run this script daily for 7 days to complete the campaign!"
