# The Unseen Portrait - Back-of-Head Photo System

An automated photo capture system that detects the back of a person's head and sends a beautifully formatted email with the captured image.

## Features

- **Back-of-Head Detection**: Uses advanced computer vision to detect only the back of the head, avoiding frontal face capture
- **Sound Notification**: Plays a sound when a photo is taken
- **Anti-Duplication**: Prevents multiple photos of the same person within a cooldown period
- **Email Integration**: Automatically sends captured photos via email with a poetic message
- **QR Code Scanning**: Optional QR code scanning for workflow integration

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. For macOS users, install zbar for QR code scanning:
```bash
brew install zbar
```

## Configuration

### Email Setup

1. **Gmail Configuration**:
   - Enable 2-factor authentication in your Gmail account
   - Generate an App Password (not your regular password)
   - Update `config.py` with your credentials

2. **QQ Email Configuration**:
   - Enable SMTP service in QQ Mail settings
   - Generate an Authorization Code
   - Update `config.py` with QQ Mail settings

### Camera Permissions

Make sure to grant camera permissions to your terminal/IDE when prompted.

## Usage

### Quick Start - Head Detection Only
```bash
python3 simple_head_test.py
```

### Complete Workflow (with email)
```bash
python3 demo_workflow.py
```

### Test Email Configuration
```bash
python3 test_email_config.py
```

## Controls

- **ESC** or **Q**: Exit the application
- **Space**: Manual photo capture (in some modes)

## Email Template

The system sends emails with the following beautiful template:

**Subject**: The Unseen Portrait

**Content**:
```
Hi,

The first glimpse
of your unseen self.

Sometimes the gentlest truths
are found
in the places we never look.

Here's to a day that feels new,
as if the world
has just begun again. 🌿

Captured on [timestamp]

Yinyin Zhou
```

## File Structure

```
backphoto/
├── config.py                 # Configuration settings
├── back_detector.py          # Core head detection logic
├── email_sender.py           # Email sending functionality
├── simple_head_test.py       # Simple head detection test
├── demo_workflow.py          # Complete workflow demo
├── test_email_config.py      # Email configuration test
├── requirements.txt          # Python dependencies
└── README_EN.md             # This file
```

## Troubleshooting

### Camera Issues
- Grant camera permissions when prompted
- Try running from terminal instead of IDE
- Check if camera is being used by other applications

### Email Issues
- Verify SMTP settings in `config.py`
- Use App Passwords for Gmail (not regular passwords)
- Check firewall settings for SMTP ports

### Detection Issues
- Ensure good lighting
- Position head within the detection area
- Avoid frontal face orientation

## Technical Details

The system uses a combination of:
- Frontal face detection (exclusion method)
- Profile face detection
- Background subtraction
- Edge detection
- Contour analysis

This ensures only the back of the head is captured, never the front face.

## Support

For issues or questions, check the configuration files and ensure all dependencies are properly installed.
