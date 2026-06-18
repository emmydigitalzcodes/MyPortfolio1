from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from .models import ContactMessage, ContactInfo, FAQ, SocialLink
from .forms import ContactForm, NewsletterForm, QuickContactForm
from .email_utils import send_contact_email, send_confirmation_email
import logging

logger = logging.getLogger('django')


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
        try:
            context['contact_info'] = ContactInfo.get_solo()
        except:
            context['contact_info'] = None
        context['faqs'] = FAQ.objects.filter(is_active=True)[:6]
        context['social_links'] = SocialLink.objects.filter(is_active=True)
        return context

    def form_valid(self, form):
        # Save the message to database
        message = form.save()

        # Send email notification to you
        send_contact_email(message)

        # Send confirmation email to the visitor
        send_confirmation_email(message)

        # Show success message
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
            contact_message = ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject='Quick Contact',
                message=form.cleaned_data['message'],
                reason='general',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                referrer=request.META.get('HTTP_REFERER', '')
            )

            # Send email for quick contact too
            send_contact_email(contact_message)

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
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip