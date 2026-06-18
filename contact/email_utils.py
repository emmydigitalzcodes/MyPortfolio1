import resend
from django.conf import settings
import logging

logger = logging.getLogger('django')


def send_contact_email(message):
    """Send contact notification email via Resend API"""
    try:
        resend.api_key = settings.RESEND_API_KEY

        params = {
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [settings.CONTACT_EMAIL],
            "subject": f"New Contact Message: {message.subject}",
            "text": f"""
You have a new contact message from your portfolio website!

-------------------------------------------
NAME:     {message.name}
EMAIL:    {message.email}
SUBJECT:  {message.subject}
REASON:   {message.get_reason_display()}
-------------------------------------------

MESSAGE:
{message.message}

-------------------------------------------
Reply directly to: {message.email}
            """,
            "reply_to": message.email,
        }

        email = resend.Emails.send(params)
        logger.info(f"Contact email sent successfully. ID: {email['id']}")
        return True

    except Exception as e:
        logger.error(f"Failed to send contact email: {e}")
        return False


def send_confirmation_email(message):
    """Send confirmation email to the person who contacted you"""
    try:
        resend.api_key = settings.RESEND_API_KEY

        params = {
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [message.email],
            "subject": "Thanks for reaching out!",
            "text": f"""
Hi {message.name},

Thank you for your message! I have received it and will get back to you as soon as possible.

Here's a copy of your message:
-------------------------------------------
Subject: {message.subject}
Message: {message.message}
-------------------------------------------

Best regards,
Chukwuemeka Moses
            """
        }

        email = resend.Emails.send(params)
        logger.info(f"Confirmation email sent to {message.email}. ID: {email['id']}")
        return True

    except Exception as e:
        logger.error(f"Failed to send confirmation email: {e}")
        return False