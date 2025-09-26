# Email Configuration Guide

This guide will help you configure email settings for the automatic photo system.

## Gmail Configuration

### Step 1: Enable 2-Factor Authentication
1. Go to your Google Account settings
2. Navigate to Security → 2-Step Verification
3. Follow the prompts to enable 2FA

### Step 2: Generate App Password
1. In Google Account settings, go to Security
2. Under "2-Step Verification", click "App passwords"
3. Select "Mail" and your device
4. Copy the generated 16-character password
5. Update `config.py`:
```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your_email@gmail.com',
    'sender_password': 'your_16_digit_app_password',  # Use the app password here
    'subject': 'The Unseen Portrait'
}
```

## QQ Mail Configuration

### Step 1: Enable SMTP Service
1. Log into QQ Mail
2. Go to Settings → Accounts
3. Enable "POP3/SMTP Service"

### Step 2: Generate Authorization Code
1. In QQ Mail settings, find "Authorization Code"
2. Click "Generate Authorization Code"
3. Follow SMS verification
4. Copy the authorization code
5. Update `config.py`:
```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.qq.com',
    'smtp_port': 587,
    'sender_email': 'your_email@qq.com',
    'sender_password': 'your_authorization_code',  # Use the authorization code here
    'subject': 'The Unseen Portrait'
}
```

## Testing Email Configuration

Run the test script to verify your email settings:
```bash
python3 test_email_config.py
```

## Common Issues

### "Username and Password not accepted"
- **Gmail**: Use App Password, not your regular password
- **QQ Mail**: Use Authorization Code, not your login password

### "Connection refused"
- Check firewall settings
- Verify SMTP server and port
- Try different network connection

### "Authentication failed"
- Ensure 2FA is enabled for Gmail
- Verify the App Password/Authorization Code is correct
- Check if the email account is locked

## Security Notes

- Never commit real passwords to version control
- Use environment variables for production
- Regularly rotate App Passwords/Authorization Codes
- Keep your email credentials secure

## Support

If you encounter issues:
1. Double-check the configuration steps
2. Verify your email provider's SMTP settings
3. Test with a simple email client first
4. Check your network connection and firewall settings
