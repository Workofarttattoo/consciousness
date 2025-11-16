# Email Consolidation - All Sites Use @aios.is

**Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved.**

## 🎯 OFFICIAL EMAIL ADDRESSES

**Primary**: inventor@aios.is
**Support**: support@aios.is
**Admin**: admin@aios.is
**Governance**: governance@aios.is

---

## 📧 EMAIL USAGE GUIDE

### inventor@aios.is
**Use for:**
- Sales inquiries
- Partnership requests
- Demo bookings
- General business contact
- Cold email replies
- **All external communications**

### support@aios.is
**Use for:**
- Customer support tickets
- Technical help
- Bug reports
- Product questions
- Onboarding assistance

### admin@aios.is
**Use for:**
- Account management
- Billing inquiries
- Subscription changes
- License management

### governance@aios.is
**Use for:**
- Legal inquiries
- Compliance questions
- Patent inquiries
- Licensing agreements
- NDA requests

---

## 🔄 FILES THAT NEED UPDATING

### aios-website Repository

**Files found with @thegavl.com or other emails:**

1. `/chrono_walker_evidence.html`
   - Line 791: `josh@thegavl.com` → `inventor@aios.is`
   - Line 842: `josh@thegavl.com` → `inventor@aios.is`

2. `/index.html`
   - Line 2322: `joshua@thegavl.com` → `inventor@aios.is`

3. `/onboarding.html`
   - Line 552: `joshua@thegavl.com` → `inventor@aios.is`
   - Line 715: `joshua@thegavl.com` → `support@aios.is` (payment support)
   - Line 728: `joshua@thegavl.com` → `support@aios.is`
   - Line 738: `joshua@thegavl.com` → `support@aios.is`
   - Line 741: `joshua@thegavl.com` → `support@aios.is`

4. `/PILOT_PROGRAM.md`
   - Line 213: `pilot@thegavl.com` → `inventor@aios.is`
   - Line 287: `pilot@thegavl.com` → `inventor@aios.is`

5. `/SUPABASE_SETUP.md`
   - Line 412: `tech@thegavl.com` → `support@aios.is`

### consciousness Repository

**Files with Calendly workofarttattoo links:**

All 20 Quantum AI cold emails have:
- `https://calendly.com/workofarttattoo/quantum-ai-demo`

**Action**: Update Calendly link to use inventor@ branding

---

## ⚡ QUICK UPDATE SCRIPT

Run this to update all files at once:

```bash
cd /Users/noone/repos/aios-website

# Update chrono_walker_evidence.html
sed -i '' 's/josh@thegavl\.com/inventor@aios.is/g' chrono_walker_evidence.html

# Update index.html
sed -i '' 's/joshua@thegavl\.com/inventor@aios.is/g' index.html

# Update onboarding.html (payment/support uses support@)
sed -i '' 's/joshua@thegavl\.com/support@aios.is/g' onboarding.html

# Update PILOT_PROGRAM.md
sed -i '' 's/pilot@thegavl\.com/inventor@aios.is/g' PILOT_PROGRAM.md

# Update SUPABASE_SETUP.md
sed -i '' 's/tech@thegavl\.com/support@aios.is/g' SUPABASE_SETUP.md
```

Then update cold emails:
```bash
cd /Users/noone/repos/consciousness

# Update Calendly link (do manually - check if workofarttattoo is correct username)
# Replace: calendly.com/workofarttattoo
# With: calendly.com/inventor-aios (or whatever you set up)
```

---

## 📋 EMAIL FORWARDING SETUP

**If you want all emails to go to one inbox:**

### Option 1: Gmail Forwarding (Free)
1. Set up inventor@aios.is as primary
2. Forward these to inventor@:
   - support@aios.is
   - admin@aios.is
   - governance@aios.is

### Option 2: Google Workspace (Recommended - $6/user/month)
1. Create Google Workspace for aios.is domain
2. Set up aliases:
   - Primary: inventor@aios.is
   - Aliases: support@, admin@, governance@
3. All emails arrive in one inbox, but you can reply as any alias

### Option 3: Email Service (Namecheap, etc.)
1. Go to domain registrar (namecheap.com)
2. Set up email forwarding rules:
   - support@aios.is → your-personal-email
   - admin@aios.is → your-personal-email
   - governance@aios.is → your-personal-email
   - inventor@aios.is → your-personal-email

---

## ✅ VERIFICATION CHECKLIST

After updates, verify:

- [ ] All @thegavl.com emails replaced
- [ ] Calendly link updated (or username correct)
- [ ] presale.html uses inventor@aios.is ✅ (already correct)
- [ ] Cold emails use inventor@aios.is ✅ (already correct)
- [ ] Email forwarding set up (all go to one inbox)
- [ ] Test email: send to inventor@aios.is, verify you receive it
- [ ] Test email: send to support@aios.is, verify you receive it

---

## 🔧 CALENDLY SETUP

**Current link in emails**: `https://calendly.com/workofarttattoo/quantum-ai-demo`

**Options:**

1. **Keep "workofarttattoo" username** (if already set up)
   - Pro: No changes needed
   - Con: Not branded as aios.is

2. **Create new Calendly with "inventor-aios" username**
   - Pro: Professional branding
   - Con: Need to update all 20 email templates
   - New link: `https://calendly.com/inventor-aios/quantum-demo`

3. **Use custom domain** (Calendly Pro - $12/mo)
   - Link: `https://calendly.aios.is/inventor`
   - Pro: Fully branded
   - Con: Requires Calendly Pro plan

**Recommendation**: Option 1 (keep workofarttattoo) for speed, upgrade to Option 3 after first customer.

---

## 📊 UPDATED EMAIL SIGNATURE

Use this signature in inventor@aios.is emails:

```
Joshua Hendricks Cole
Inventor & CEO
Corporation of Light

🌐 aios.is
📧 inventor@aios.is
📅 Book a demo: calendly.com/workofarttattoo/quantum-demo

Quantum-Enhanced AI | Patent Pending
```

---

**Status**: ✅ UPDATE PLAN COMPLETE
**Action**: Run bash commands above to update all files
**Estimated time**: 5 minutes
