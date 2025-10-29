# Google Calendar Appointment Scheduling Setup

**Quick guide to set up your demo booking calendar**

---

## Step 1: Create Appointment Schedule

1. Go to **Google Calendar**: https://calendar.google.com
2. Click the **Settings gear icon** (top right) → **Settings**
3. In the left sidebar, click **Appointment schedules**
4. Click **+ Create**

---

## Step 2: Configure Your Booking Page

### Basic Settings
- **Name**: "Quantum-Enhanced AI Demo"
- **Duration**: 30 minutes (for 10-minute demo + buffer)
- **Location**: Google Meet (automatically generated)

### Availability
- **Booking window**: 1-30 days in advance
- **Available hours**:
  - Monday-Friday: 9:00 AM - 5:00 PM (adjust to your timezone)
  - Buffer between appointments: 15 minutes
  - Max bookings per day: 4 (to avoid burnout)

### Booking Form (Custom Questions)
Add these questions for qualification:
1. **Company Name** (required)
2. **Your Role/Title** (required)
3. **Industry** (dropdown: Drug Discovery, Finance, Logistics, Materials Science, Other)
4. **Specific Use Case** (text area): "What optimization problem are you trying to solve?"
5. **Team Size** (optional): "How many people will join the demo?"

### Notifications
- **Email confirmations**: Enabled
- **Reminders**: 1 hour before, 1 day before
- **Timezone display**: Automatically detect visitor's timezone

---

## Step 3: Get Your Booking Link

1. After creating the schedule, Google will generate a booking URL like:
   ```
   https://calendar.google.com/calendar/appointments/schedules/[YOUR-SCHEDULE-ID]
   ```

2. **Copy this full URL** and replace the placeholder in your sales materials:
   - `QUANTUM_ECH0_SALES_SHEET.md` (line 187)
   - `quantum_ech0_landing_page.html` (search for "calendar.google.com")

---

## Step 4: Customize Booking Page (Optional)

### Appearance
- **Page title**: "Book Your Quantum-Enhanced AI Demo"
- **Description**:
  ```
  10-minute live demonstration of our quantum-enhanced AI achieving 12.54x speedup.

  You'll see:
  - Live quantum entanglement (Bell state)
  - 12x speedup benchmark in real-time
  - Your specific use case analyzed

  No slides - just working code and results.
  ```

### Confirmation Email
Customize the auto-reply email sent after booking:
```
Subject: Your Quantum-Enhanced AI Demo is Confirmed

Hi [Name],

Your demo is confirmed for [Date/Time].

What to expect:
- 10-minute live demo (no slides, working code)
- See 12.54x speedup in real-time
- Your use case analyzed on the spot
- Q&A with technical team

Meeting link: [Google Meet auto-generated]

Preparation (optional):
- Review our technical paper: https://github.com/workofarttattoo/consciousness
- Think about your specific optimization challenges
- Bring questions!

Questions before the demo? Reply to this email.

Looking forward to showing you what quantum-enhanced AI can do!

Best,
Joshua Hendricks Cole
Corporation of Light
inventor@aios.is
```

---

## Step 5: Test Your Booking Page

1. Open your booking link in an **incognito/private browser window**
2. Book a test appointment to see the user experience
3. Check that:
   - Custom questions appear correctly
   - Confirmation email arrives (check spam folder)
   - Google Meet link is generated
   - Calendar event appears in your calendar

4. **Cancel the test appointment** after verifying

---

## Step 6: Integrate with Sales Materials

### Update these files with your booking link:

1. **QUANTUM_ECH0_SALES_SHEET.md**
   - Line 187: Replace `[YOUR-SCHEDULE-ID]` with actual ID

2. **quantum_ech0_landing_page.html**
   - No changes needed - form sends email directly to inventor@aios.is
   - You can add booking link to confirmation email if desired

3. **OUTREACH_TEMPLATES.md**
   - Replace `[calendar link]` placeholders with your URL
   - Add to email signatures: "📅 Book demo: [your booking link]"

---

## Pro Tips

### Qualification Pre-Screening
In your custom questions, add:
> "What's your approximate budget for AI optimization tools?"
> - Options: Under $10K, $10K-$50K, $50K-$100K, $100K+, Not sure yet

This helps prioritize high-value leads.

### Automated Follow-Up
After demo appointment is booked:
1. Send **pre-demo email 24 hours before** with:
   - Technical paper link
   - Brief agenda
   - Request to share specific use case in advance

2. **Post-demo follow-up** (manually send within 1 hour):
   - Summary of what they saw
   - Pricing reminder
   - Next steps (contract, POC, technical deep-dive)

### Calendar Buffer Management
- **Before demos**: 15-minute buffer to prepare (test scripts, review notes)
- **After demos**: 15-minute buffer for follow-up email and notes
- **Lunch break**: Block 12-1 PM to avoid back-to-back demos

### No-Show Prevention
- Enable **SMS reminders** if available (Google Calendar supports this)
- Send manual reminder **2 hours before** for first-time demos
- Follow up with no-shows: "Missed you today - reschedule link: [booking URL]"

---

## Tracking Demo Metrics

Create a simple spreadsheet to track:

| Date | Company | Contact | Industry | Use Case | Attended? | Next Step | Status |
|------|---------|---------|----------|----------|-----------|-----------|--------|
| 11/1 | Acme | John Doe | Pharma | Molecule screening | Yes | Sent proposal | In Progress |

This helps you identify:
- **No-show rate** (target: <10%)
- **Demo → Close rate** (target: 20-30%)
- **Best-performing industries** (double down on these)
- **Common objections** (prepare better answers)

---

## Alternative: Calendly (If Google Calendar Doesn't Work)

If you prefer a dedicated booking tool:
1. Sign up for **Calendly** (free plan works): https://calendly.com
2. Connect your Google Calendar
3. Create "Quantum AI Demo" event type
4. Use Calendly link instead: `https://calendly.com/[your-username]/quantum-ai-demo`

**Pros**: More customization options, better analytics
**Cons**: Another tool to manage, free plan has "Powered by Calendly" branding

---

## Quick Start (If You're in a Hurry)

**5-Minute Setup**:
1. Google Calendar → Settings → Appointment schedules → Create
2. Name: "Quantum AI Demo", Duration: 30 min, Location: Google Meet
3. Availability: Mon-Fri 9-5, Buffer: 15 min, Max: 4/day
4. Copy booking link
5. Update QUANTUM_ECH0_SALES_SHEET.md with link
6. Test in incognito window
7. Start sending to prospects!

---

## Your Booking Link Template

Once set up, use this in all outreach:

```
📅 **Book your free 10-minute demo**: https://calendar.google.com/calendar/appointments/schedules/[YOUR-SCHEDULE-ID]

See quantum-enhanced AI achieve 12.54x speedup live - no slides, just working code.
```

---

**Status**: Follow this guide to set up your booking calendar, then update the sales materials with your actual booking URL.

**Estimated time**: 10-15 minutes for full setup.
