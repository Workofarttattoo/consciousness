/*
 * Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.
 *
 * Sovereign Security Toolkit - Square Payment Backend
 * Handles payment processing, license generation, and email delivery
 */

const express = require('express');
const { Client, Environment } = require('square');
const crypto = require('crypto');
const nodemailer = require('nodemailer');
const path = require('path');

const app = express();
app.use(express.json());
app.use(express.static('.')); // Serve HTML files

// Square client configuration
const squareClient = new Client({
  environment: Environment.Sandbox, // Change to Environment.Production for live
  accessToken: process.env.SQUARE_ACCESS_TOKEN || 'YOUR_SQUARE_ACCESS_TOKEN_HERE'
});

// Email configuration (using Gmail as example)
const emailTransporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.EMAIL_USER || 'your-email@gmail.com',
    pass: process.env.EMAIL_PASSWORD || 'your-app-password'
  }
});

// Pricing configuration
const PRICING = {
  pro: {
    name: 'Professional',
    price: 299,
    features: [
      'All 18 security tools',
      'Unlimited assessments',
      'Forensic mode included',
      'JSON/HTML reports',
      'Priority email support',
      'Lifetime updates',
      'Commercial use license'
    ]
  },
  enterprise: {
    name: 'Enterprise',
    price: 4999,
    features: [
      'Everything in Professional',
      'Multi-user licenses (10 seats)',
      'Custom tool integration',
      'API access for automation',
      'White-label reporting',
      '24/7 phone support',
      'Training & onboarding',
      'Custom development (20 hours)'
    ]
  }
};

/**
 * Generate a unique license key
 */
function generateLicenseKey(plan) {
  const prefix = plan === 'pro' ? 'SOVPRO' : 'SOVENT';
  const random = crypto.randomBytes(8).toString('hex').toUpperCase();
  return `${prefix}-${random.slice(0, 4)}-${random.slice(4, 8)}-${random.slice(8, 12)}`;
}

/**
 * Process Square payment
 */
app.post('/api/process-payment', async (req, res) => {
  try {
    const { token, amount, plan } = req.body;

    // Validate plan
    if (!PRICING[plan]) {
      return res.status(400).json({
        success: false,
        error: 'Invalid plan selected'
      });
    }

    const planDetails = PRICING[plan];

    // Validate amount matches plan price
    if (amount !== planDetails.price * 100) {
      return res.status(400).json({
        success: false,
        error: 'Amount mismatch'
      });
    }

    // Create idempotency key for payment
    const idempotencyKey = crypto.randomUUID();

    // Process payment with Square
    const paymentResponse = await squareClient.paymentsApi.createPayment({
      sourceId: token,
      idempotencyKey: idempotencyKey,
      amountMoney: {
        amount: BigInt(amount),
        currency: 'USD'
      },
      note: `Sovereign Security Toolkit - ${planDetails.name} Plan`,
      autocomplete: true
    });

    if (paymentResponse.result.payment.status === 'COMPLETED') {
      const payment = paymentResponse.result.payment;

      // Generate license key
      const licenseKey = generateLicenseKey(plan);

      // Store license in database (implement your DB logic here)
      await storeLicense({
        licenseKey,
        plan,
        paymentId: payment.id,
        amount: planDetails.price,
        createdAt: new Date(),
        status: 'active'
      });

      // Send confirmation email
      await sendLicenseEmail({
        email: payment.buyerEmailAddress || 'customer@example.com',
        licenseKey,
        plan: planDetails.name,
        features: planDetails.features
      });

      // Return success response
      return res.json({
        success: true,
        orderId: payment.id,
        licenseKey: licenseKey,
        message: 'Payment successful'
      });
    } else {
      return res.status(400).json({
        success: false,
        error: 'Payment not completed'
      });
    }

  } catch (error) {
    console.error('Payment processing error:', error);
    return res.status(500).json({
      success: false,
      error: error.message || 'Payment processing failed'
    });
  }
});

/**
 * Store license in database
 * TODO: Implement with your preferred database (MongoDB, PostgreSQL, etc.)
 */
async function storeLicense(licenseData) {
  // Example: Save to JSON file (replace with real database)
  const fs = require('fs').promises;
  const licensesFile = path.join(__dirname, 'licenses.json');

  try {
    let licenses = [];
    try {
      const data = await fs.readFile(licensesFile, 'utf8');
      licenses = JSON.parse(data);
    } catch (err) {
      // File doesn't exist yet
    }

    licenses.push(licenseData);
    await fs.writeFile(licensesFile, JSON.stringify(licenses, null, 2));

    console.log('License stored:', licenseData.licenseKey);
  } catch (error) {
    console.error('Error storing license:', error);
    throw error;
  }
}

/**
 * Send license email to customer
 */
async function sendLicenseEmail({ email, licenseKey, plan, features }) {
  const emailHTML = `
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; background: #fff; padding: 40px; border-radius: 10px; }
        h1 { color: #00ff88; }
        .license-box { background: #f9f9f9; border: 2px solid #00ff88; padding: 20px; border-radius: 5px; margin: 20px 0; }
        .license-key { font-size: 24px; font-weight: bold; color: #00ccff; letter-spacing: 2px; text-align: center; }
        .features { list-style: none; padding: 0; }
        .features li { padding: 10px 0; border-bottom: 1px solid #eee; }
        .features li:before { content: '✓ '; color: #00ff88; font-weight: bold; }
        .footer { margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #666; }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>🎉 Welcome to Sovereign Security Toolkit!</h1>
        <p>Thank you for your purchase of the <strong>${plan} Plan</strong>.</p>

        <div class="license-box">
          <p style="margin: 0 0 10px 0; color: #666;">Your License Key:</p>
          <div class="license-key">${licenseKey}</div>
        </div>

        <h2>Your Plan Includes:</h2>
        <ul class="features">
          ${features.map(f => `<li>${f}</li>`).join('')}
        </ul>

        <h2>Getting Started:</h2>
        <ol>
          <li>Download the toolkit from: <a href="https://red-team-tools.aios.is/download">red-team-tools.aios.is/download</a></li>
          <li>Install following the README instructions</li>
          <li>Enter your license key when prompted</li>
          <li>Start your first security assessment!</li>
        </ol>

        <p><strong>Need Help?</strong></p>
        <p>
          • Documentation: <a href="https://red-team-tools.aios.is/docs">red-team-tools.aios.is/docs</a><br>
          • Support Email: support@sovereignsecurity.io<br>
          • Professional Plan: Response within 24 hours
        </p>

        <div class="footer">
          <p>Copyright © 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.</p>
          <p>This license is non-transferable and for your use only.</p>
        </div>
      </div>
    </body>
    </html>
  `;

  try {
    await emailTransporter.sendMail({
      from: '"Sovereign Security" <noreply@sovereignsecurity.io>',
      to: email,
      subject: `Your Sovereign Security ${plan} License - ${licenseKey}`,
      html: emailHTML
    });

    console.log('License email sent to:', email);
  } catch (error) {
    console.error('Error sending email:', error);
    // Don't throw - payment already succeeded
  }
}

/**
 * Verify license endpoint
 */
app.post('/api/verify-license', async (req, res) => {
  try {
    const { licenseKey } = req.body;

    // Load licenses from database
    const fs = require('fs').promises;
    const licensesFile = path.join(__dirname, 'licenses.json');

    try {
      const data = await fs.readFile(licensesFile, 'utf8');
      const licenses = JSON.parse(data);

      const license = licenses.find(l => l.licenseKey === licenseKey && l.status === 'active');

      if (license) {
        return res.json({
          valid: true,
          plan: license.plan,
          createdAt: license.createdAt
        });
      } else {
        return res.json({
          valid: false,
          error: 'Invalid or expired license'
        });
      }
    } catch (err) {
      return res.status(500).json({
        valid: false,
        error: 'License verification failed'
      });
    }

  } catch (error) {
    console.error('License verification error:', error);
    return res.status(500).json({
      valid: false,
      error: error.message
    });
  }
});

/**
 * Webhook endpoint for Square events
 */
app.post('/api/square-webhook', async (req, res) => {
  try {
    const signature = req.headers['x-square-signature'];
    const body = JSON.stringify(req.body);

    // Verify webhook signature (important for security)
    // Implement signature verification based on Square docs

    const event = req.body;

    console.log('Square webhook event:', event.type);

    // Handle different event types
    switch (event.type) {
      case 'payment.created':
        console.log('Payment created:', event.data.object.payment.id);
        break;
      case 'payment.updated':
        console.log('Payment updated:', event.data.object.payment.id);
        break;
      case 'refund.created':
        // Deactivate license on refund
        const refund = event.data.object.refund;
        await deactivateLicense(refund.payment_id);
        break;
    }

    res.json({ success: true });
  } catch (error) {
    console.error('Webhook error:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * Deactivate license (for refunds)
 */
async function deactivateLicense(paymentId) {
  const fs = require('fs').promises;
  const licensesFile = path.join(__dirname, 'licenses.json');

  try {
    const data = await fs.readFile(licensesFile, 'utf8');
    const licenses = JSON.parse(data);

    const license = licenses.find(l => l.paymentId === paymentId);
    if (license) {
      license.status = 'revoked';
      license.revokedAt = new Date();
      await fs.writeFile(licensesFile, JSON.stringify(licenses, null, 2));
      console.log('License revoked:', license.licenseKey);
    }
  } catch (error) {
    console.error('Error deactivating license:', error);
  }
}

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    service: 'Sovereign Security Payment Server',
    timestamp: new Date().toISOString()
  });
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════════════════════╗
║  Sovereign Security Payment Server                        ║
║  Copyright © 2025 Corporation of Light                    ║
╚═══════════════════════════════════════════════════════════╝

✓ Server running on port ${PORT}
✓ Square environment: ${process.env.SQUARE_ACCESS_TOKEN ? 'Configured' : 'NOT CONFIGURED'}
✓ Email service: ${process.env.EMAIL_USER ? 'Configured' : 'NOT CONFIGURED'}

Endpoints:
  POST /api/process-payment     - Process Square payments
  POST /api/verify-license      - Verify license keys
  POST /api/square-webhook      - Square webhook handler
  GET  /api/health              - Health check

Open http://localhost:${PORT}/SOVEREIGN_SECURITY_LANDING.html to view the landing page.
  `);
});

module.exports = app;
