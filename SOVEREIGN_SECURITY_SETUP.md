# Sovereign Security Toolkit - Square Payment Setup Guide

Copyright © 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

## 🚀 Complete Setup Guide

This guide will help you launch the Sovereign Security business with Square payments in **2 weeks**.

---

## Phase 1: Square Account Setup (Day 1)

### 1.1 Create Square Developer Account

1. Go to https://developer.squareup.com/
2. Sign up for a free developer account
3. Create a new application: "Sovereign Security Toolkit"
4. Note your credentials:
   - **Application ID**: `sq0idp-XXXXX` (for frontend)
   - **Access Token**: `EAAAxxxx` (for backend)
   - **Location ID**: `LXXXXX` (your business location)

### 1.2 Configure Square Sandbox (Testing)

```bash
# Your Square sandbox credentials (for testing)
Application ID: sandbox-sq0idb-XXXXX
Access Token: EAAAExxxxxx (sandbox)
```

**Note:** Sandbox mode lets you test payments without real money.

### 1.3 Go Live Checklist

When ready for production:
- ✅ Complete Square account verification
- ✅ Activate payment processing
- ✅ Update `sovereign_security_payment_server.js`:
  - Change `Environment.Sandbox` to `Environment.Production`
  - Update access token to production token
- ✅ Update `SOVEREIGN_SECURITY_LANDING.html`:
  - Change application ID to production ID

---

## Phase 2: Backend Setup (Day 2)

### 2.1 Install Dependencies

```bash
cd /Users/noone/consciousness

# Install Node.js dependencies
npm install express square nodemailer
```

### 2.2 Configure Environment Variables

Create `.env` file:

```bash
# Square Configuration
SQUARE_ACCESS_TOKEN=EAAAxxxxxxxxxxxxxxx
SQUARE_APPLICATION_ID=sq0idp-xxxxxxxxxxxxx
SQUARE_LOCATION_ID=Lxxxxxxxxxxxxxxx

# Email Configuration (Gmail example)
EMAIL_USER=your-business-email@gmail.com
EMAIL_PASSWORD=your-app-specific-password

# Server Configuration
PORT=3000
NODE_ENV=production
```

**Gmail App Password Setup:**
1. Go to Google Account → Security
2. Enable 2-Step Verification
3. Generate App Password for "Mail"
4. Use that password in `.env`

### 2.3 Update Landing Page

Edit `SOVEREIGN_SECURITY_LANDING.html` line 473:

```javascript
// BEFORE:
const applicationId = 'sandbox-sq0idb-XXXXX'; // REPLACE THIS
const locationId = 'LXXXXX'; // REPLACE THIS

// AFTER (with your real values):
const applicationId = 'sq0idp-YOUR_ACTUAL_APP_ID';
const locationId = 'LYOUR_ACTUAL_LOCATION';
```

---

## Phase 3: Testing (Day 3)

### 3.1 Start the Server

```bash
cd /Users/noone/consciousness
node sovereign_security_payment_server.js
```

You should see:

```
╔═══════════════════════════════════════════════════════════╗
║  Sovereign Security Payment Server                        ║
║  Copyright © 2025 Corporation of Light                    ║
╚═══════════════════════════════════════════════════════════╝

✓ Server running on port 3000
✓ Square environment: Configured
✓ Email service: Configured
```

### 3.2 Test Payment Flow

1. Open browser: http://localhost:3000/SOVEREIGN_SECURITY_LANDING.html
2. Click "Buy Professional" ($299)
3. Use Square test card:
   - **Card Number**: 4111 1111 1111 1111
   - **Expiry**: Any future date
   - **CVV**: Any 3 digits
   - **ZIP**: Any 5 digits

4. Verify:
   - ✅ Payment processes successfully
   - ✅ License key generated
   - ✅ Email sent with license
   - ✅ License saved to `licenses.json`

### 3.3 Test License Verification

```bash
curl -X POST http://localhost:3000/api/verify-license \
  -H "Content-Type: application/json" \
  -d '{"licenseKey": "SOVPRO-XXXX-XXXX-XXXX"}'
```

Should return:
```json
{
  "valid": true,
  "plan": "pro",
  "createdAt": "2025-10-27T..."
}
```

---

## Phase 4: Deploy to Production (Day 4-5)

### 4.1 Choose Hosting Provider

**Option A: DigitalOcean (Recommended - $12/month)**

```bash
# Create Droplet (Ubuntu 24.04)
# Install Node.js and PM2
ssh root@your-server-ip

apt update && apt upgrade -y
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs
npm install -g pm2

# Upload your files
scp -r sovereign_* root@your-server-ip:/root/
```

**Option B: Heroku (Free tier available)**

```bash
# Install Heroku CLI
brew install heroku/brew/heroku

# Deploy
heroku create sovereign-security
git add .
git commit -m "Deploy Sovereign Security"
git push heroku main
```

**Option C: Netlify + Serverless Functions (Free tier)**

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod
```

### 4.2 Configure Domain

1. Buy domain (recommend: sovereignsecurity.io or use existing red-team-tools.aios.is)
2. Point DNS to your server:
   ```
   A record: @ → your-server-ip
   A record: www → your-server-ip
   ```

3. Install SSL certificate (Let's Encrypt):
   ```bash
   apt install certbot python3-certbot-nginx
   certbot --nginx -d sovereignsecurity.io -d www.sovereignsecurity.io
   ```

### 4.3 Production Server Setup

```bash
# On your server
cd /root
git clone YOUR_REPO
cd consciousness

# Install dependencies
npm install --production

# Set environment variables
cat > .env << EOF
SQUARE_ACCESS_TOKEN=your-production-token
SQUARE_APPLICATION_ID=your-production-app-id
SQUARE_LOCATION_ID=your-production-location-id
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
NODE_ENV=production
PORT=3000
EOF

# Start with PM2 (auto-restart)
pm2 start sovereign_security_payment_server.js --name sovereign-security
pm2 save
pm2 startup
```

### 4.4 Setup Nginx Reverse Proxy

```bash
cat > /etc/nginx/sites-available/sovereign << EOF
server {
    listen 80;
    server_name sovereignsecurity.io www.sovereignsecurity.io;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

ln -s /etc/nginx/sites-available/sovereign /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

---

## Phase 5: Marketing & Launch (Day 6-14)

### 5.1 Update Landing Page with Live URL

Change all references from `localhost:3000` to `https://sovereignsecurity.io`

### 5.2 Create Marketing Materials

**Already Created (in `/Users/noone/consciousness/marketing/`):**
- ✅ Instagram ads (1080x1080px)
- ✅ Facebook ads
- ✅ Landing page with Square integration

**To Create:**
1. **Twitter/X Thread**
   ```
   🚀 Launching Sovereign Security Toolkit

   18 professional security tools
   - Network recon
   - DB injection analysis
   - Wireless auditing
   - Credential analysis
   - And 14 more...

   $24K value → $299
   98.8% discount

   Get it: sovereignsecurity.io
   ```

2. **LinkedIn Post**
   ```
   After 5 years in security consulting, I've built the toolkit I wish I had.

   Sovereign Security Toolkit: 18 professional tools for $299 (normally $24K).

   Built for: Pentesters, security researchers, IT teams

   Features:
   - Read-only forensic mode
   - JSON/HTML reports
   - Offline operation
   - Zero dependencies on cloud services

   Launch sale: First 100 licenses → 50% off
   [Link to sovereignsecurity.io]
   ```

3. **Reddit Posts**
   - r/netsec
   - r/AskNetsec
   - r/cybersecurity
   - r/hacking

### 5.3 Launch Strategy

**Week 1 (Soft Launch)**
- Email existing contacts
- Post on LinkedIn, Twitter
- Reach out to 10 security professionals for testimonials
- Target: 5-10 sales ($1,500-3,000)

**Week 2 (Hard Launch)**
- Product Hunt launch
- Reddit posts
- Paid ads ($50/day Facebook, $30/day Google)
- Partnerships with security bloggers
- Target: 20-30 sales ($6,000-9,000)

**Month 1 Goal:** 50 Professional licenses = $14,950 revenue

---

## Phase 6: Post-Launch Operations

### 6.1 Customer Support

**Email Template (saved in support@sovereignsecurity.io):**

```
Subject: Re: Sovereign Security Support - [Ticket #XXXX]

Hi [Name],

Thank you for reaching out!

[Answer to their question]

Additional resources:
- Documentation: https://sovereignsecurity.io/docs
- Community: https://discord.gg/sovereign-security
- Video tutorials: https://youtube.com/@sovereignsecurity

Best regards,
Josh
Corporation of Light
```

### 6.2 License Management

Check licenses:
```bash
# View all licenses
cat licenses.json | jq '.[] | {licenseKey, plan, status}'

# Count active licenses
cat licenses.json | jq '[.[] | select(.status == "active")] | length'

# Total revenue
cat licenses.json | jq '[.[] | .amount] | add'
```

### 6.3 Monitoring

**Server Health:**
```bash
# CPU, memory, disk
pm2 monit

# Server logs
pm2 logs sovereign-security

# Error tracking
tail -f /var/log/nginx/error.log
```

**Payment Analytics:**
- Login to Square Dashboard: https://squareup.com/dashboard
- View transactions, refunds, chargebacks
- Export reports for accounting

---

## Revenue Projections

### Conservative (First Year)

| Month | Pro ($299) | Enterprise ($4,999) | Revenue  |
|-------|------------|---------------------|----------|
| 1     | 50         | 0                   | $14,950  |
| 2     | 40         | 1                   | $16,959  |
| 3     | 30         | 2                   | $18,958  |
| 4-6   | 25/mo      | 1/mo                | $27,468  |
| 7-12  | 20/mo      | 1/mo                | $35,928  |
| **Total Year 1** |              |         | **$114,263** |

### Aggressive (Best Case)

| Month | Pro ($299) | Enterprise ($4,999) | Revenue  |
|-------|------------|---------------------|----------|
| 1     | 100        | 2                   | $39,898  |
| 2     | 80         | 3                   | $38,897  |
| 3     | 60         | 5                   | $42,915  |
| 4-12  | 40/mo      | 3/mo                | $161,928 |
| **Total Year 1** |              |         | **$283,638** |

---

## Troubleshooting

### Payment Not Processing

**Check:**
1. Square credentials correct in `.env`
2. Server running: `pm2 list`
3. Logs: `pm2 logs sovereign-security`
4. Browser console for JavaScript errors

**Common Issues:**
- Expired sandbox credentials (regenerate every 90 days)
- Missing environment variables
- CORS errors (add domain to Square dashboard)

### Email Not Sending

**Check:**
1. Gmail app password correct
2. 2-Step Verification enabled on Google account
3. "Less secure app access" NOT required with app password

**Test email:**
```bash
curl -X POST http://localhost:3000/api/process-payment \
  -H "Content-Type: application/json" \
  -d '{"token":"test","amount":29900,"plan":"pro"}'
```

### License Verification Failing

**Check:**
1. `licenses.json` exists and readable
2. License key format correct: `SOVPRO-XXXX-XXXX-XXXX`
3. License status is "active" (not "revoked")

---

## Next Steps

✅ **Day 1:** Setup Square account
✅ **Day 2:** Configure backend server
✅ **Day 3:** Test payment flow end-to-end
✅ **Day 4-5:** Deploy to production server
✅ **Day 6-7:** Create marketing content
✅ **Day 8:** Soft launch to email list
✅ **Day 9-14:** Hard launch (Product Hunt, Reddit, ads)

**Target:** $15K revenue in first month, $100K+ Year 1

---

## Support & Resources

- **Documentation:** This file + inline code comments
- **Square API Docs:** https://developer.squareup.com/docs
- **Node.js Express:** https://expressjs.com/
- **PM2 Process Manager:** https://pm2.keymetrics.io/

**Questions?**
Email: josh@corporationoflight.com
