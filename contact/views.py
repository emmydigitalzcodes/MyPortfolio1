from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import ContactMessage, ContactInfo, FAQ, SocialLink
from .forms import ContactForm, NewsletterForm, QuickContactForm


class ContactView(FormView):
    """Contact page view with form"""
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = '/contact/success/'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get contact info
        try:
            context['contact_info'] = ContactInfo.get_solo()
        except:
            context['contact_info'] = None
        
        # Get FAQs
        context['faqs'] = FAQ.objects.filter(is_active=True)[:6]
        
        # Get social links
        context['social_links'] = SocialLink.objects.filter(is_active=True)
        
        return context
    
    def form_valid(self, form):
        # Save the message
        message = form.save()
        
        # Send email notification
        self.send_notification_email(message)
        
        # Add success message
        messages.success(
            self.request,
            'Thank you for your message! I will get back to you soon.'
        )
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            'Please correct the errors below and try again.'
        )
        return super().form_invalid(form)
    
    def send_notification_email(self, message):
        """Send email notification for new contact message"""
        try:
            subject = f"New Contact Message: {message.subject}"
            body = f"""
New contact message received:

From: {message.name} <{message.email}>
Subject: {message.subject}
Reason: {message.get_reason_display()}

Message:
{message.message}

---
Reply to: {message.email}
            """
            
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=True
            )
        except Exception as e:
            # Log the error but don't fail the form submission
            import logging
            logger = logging.getLogger('django')
            logger.error(f"Failed to send contact notification email: {e}")


class ContactSuccessView(TemplateView):
    """Contact form success page"""
    template_name = 'contact/contact_success.html'


class FAQView(TemplateView):
    """FAQ page view"""
    template_name = 'contact/faq.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = FAQ.objects.filter(is_active=True)
        return context


def quick_contact(request):
    """AJAX quick contact form handler"""
    if request.method == 'POST':
        form = QuickContactForm(request.POST)
        
        if form.is_valid():
            # Create contact message
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject='Quick Contact',
                message=form.cleaned_data['message'],
                reason='general',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                referrer=request.META.get('HTTP_REFERER', '')
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Thank you! Your message has been sent.'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=405)


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
