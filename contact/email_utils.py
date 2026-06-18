import resend
from django.conf import settings

resend.api_key = settings.RESEND_API_KEY

def send_contact_email(message):
    try:
        resend.Emails.send({
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": settings.CONTACT_EMAIL,
            "subject": f"New Contact Message: {message.subject}",
            "text": f"""
From: {message.name} <{message.email}>
Subject: {message.subject}

Message:
{message.message}

Reply to: {message.email}
            """
        })
        return True
    except Exception as e:
        import logging
        logging.getLogger('django').error(f"Email failed: {e}")
        return False