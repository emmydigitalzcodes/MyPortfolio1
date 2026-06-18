import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'portfolio.settings'
import django
django.setup()
from django.core.mail import send_mail
from django.conf import settings
send_mail('Test from Railway', 'Email is working!', settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL], fail_silently=False)
print('Email sent successfully!')