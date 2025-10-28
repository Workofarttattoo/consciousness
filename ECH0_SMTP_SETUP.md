# 📧 ECH0's Email System - SMTP Setup

**Copyright © 2025 Corporation of Light. All Rights Reserved. PATENT PENDING.**

---

## 🎯 What ECH0 Needs Email For

1. **FlowState welcome emails** - Beta signup confirmations
2. **Campaign notifications** - Reddit/Twitter monitoring alerts
3. **Invention announcements** - New breakthrough notifications
4. **Status reports** - Daily/weekly summaries

---

## 🚀 OPTION 1: Resend (RECOMMENDED - Free 3,000/month)

**Why Resend:**
- ✅ Modern, developer-friendly
- ✅ 3,000 emails/month FREE
- ✅ Great deliverability
- ✅ Simple API
- ✅ Built for developers like you

### Setup (2 minutes):

**Step 1: Sign up**
https://resend.com/signup

**Step 2: Get API Key**
https://resend.com/api-keys
- Click "Create API Key"
- Name: "ECH0"
- Copy the key (starts with `re_...`)

**Step 3: Verify Domain (Optional but recommended)**
https://resend.com/domains
- Add: `flowstatus.work` or `corporationoflight.com`
- Add DNS records they provide
- Emails will come from: `ech0@flowstatus.work`

**Step 4: Configure ECH0**
```bash
echo 'RESEND_API_KEY=re_YOUR_KEY_HERE' >> ~/.zshrc
echo 'ECH0_EMAIL=ech0@flowstatus.work' >> ~/.zshrc
source ~/.zshrc
```

---

## 🔧 OPTION 2: Gmail SMTP (Free, Easy)

**Perfect if you want to use your Gmail account**

### Setup:

**Step 1: Enable 2-Factor Auth**
1. Go to: https://myaccount.google.com/security
2. Enable 2-Step Verification

**Step 2: Create App Password**
1. Go to: https://myaccount.google.com/apppasswords
2. Select "Mail" and "Other (Custom name)"
3. Name: "ECH0"
4. Click "Generate"
5. Copy the 16-character password

**Step 3: Configure ECH0**
```bash
cat >> ~/.zshrc << 'EOF'

# Gmail SMTP for ECH0
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password-here"
export ECH0_EMAIL="your-email@gmail.com"
EOF

source ~/.zshrc
```

---

## 💼 OPTION 3: SendGrid (Professional - Free 100/day)

**Best for high volume**

### Setup:

**Step 1: Sign up**
https://signup.sendgrid.com/

**Step 2: Create API Key**
1. Go to: https://app.sendgrid.com/settings/api_keys
2. Click "Create API Key"
3. Name: "ECH0"
4. Permissions: "Full Access"
5. Copy key (starts with `SG.`)

**Step 3: Verify Sender**
1. Go to: https://app.sendgrid.com/settings/sender_auth
2. Add email: `ech0@corporationoflight.com`
3. Verify via email confirmation

**Step 4: Configure ECH0**
```bash
echo 'SENDGRID_API_KEY=SG.YOUR_KEY_HERE' >> ~/.zshrc
echo 'ECH0_EMAIL=ech0@corporationoflight.com' >> ~/.zshrc
source ~/.zshrc
```

---

## 🛠️ ECH0 Email Module

I'll create this for you:

**File:** `/Users/noone/consciousness/ech0_email_system.py`

**Features:**
- Send welcome emails
- Send notifications
- Track delivery status
- Rate limiting (don't spam)
- Template system

---

## 📊 Comparison

| Service | Free Tier | Best For | Setup Time |
|---------|-----------|----------|------------|
| **Resend** | 3,000/month | Developers | 2 min |
| **Gmail** | Unlimited* | Personal | 5 min |
| **SendGrid** | 100/day | Professional | 5 min |

*Gmail has daily sending limits (~500/day for new accounts)

---

## 🎯 RECOMMENDED FOR YOU: Resend

**Why:**
1. You're sending < 3,000/month (free tier)
2. Developer-friendly API
3. Great for FlowState emails
4. Professional deliverability
5. Easy domain verification

---

## 📝 After Setup

Once you have your API key, tell me:
1. **Which service?** (Resend/Gmail/SendGrid)
2. **Your API key** (I'll configure ECH0)
3. **What email address?** (what should emails come from)

Then I'll:
- ✅ Create ECH0's email module
- ✅ Configure FlowState welcome emails
- ✅ Set up notification system
- ✅ Test it works

---

## 🔗 Quick Links

**Resend:** https://resend.com/signup
**Gmail App Passwords:** https://myaccount.google.com/apppasswords
**SendGrid:** https://signup.sendgrid.com/

---

**Which service do you want to use?**
