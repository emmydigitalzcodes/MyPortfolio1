from django import forms
from django.core.validators import EmailValidator
from .models import ContactMessage
from blog.models import NewsletterSubscriber


class ContactForm(forms.ModelForm):
    """Contact form with validation"""
    
    # reCAPTCHA field (will be rendered in template)
    recaptcha_token = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'company', 'subject', 'message', 'reason']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'autocomplete': 'name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'autocomplete': 'email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 (555) 123-4567',
                'autocomplete': 'tel'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Company (optional)',
                'autocomplete': 'organization'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Message Subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your message...',
                'rows': 6
            }),
            'reason': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Make fields optional except required ones
        self.fields['phone'].required = False
        self.fields['company'].required = False
        
        # Add help texts
        self.fields['name'].help_text = 'Your full name'
        self.fields['email'].help_text = 'We will never share your email'
        self.fields['message'].help_text = 'Minimum 20 characters'
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name.strip()) < 2:
            raise forms.ValidationError('Name must be at least 2 characters long.')
        return name.strip()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.lower().strip()
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message.strip()) < 20:
            raise forms.ValidationError('Message must be at least 20 characters long.')
        return message.strip()
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Additional validation can be added here
        # For example, checking for spam keywords
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Add request metadata
        if self.request:
            instance.ip_address = self.get_client_ip()
            instance.user_agent = self.request.META.get('HTTP_USER_AGENT', '')
            instance.referrer = self.request.META.get('HTTP_REFERER', '')
        
        if commit:
            instance.save()
        
        return instance
    
    def get_client_ip(self):
        """Get client IP address from request"""
        if not self.request:
            return None
        
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class NewsletterForm(forms.ModelForm):
    """Newsletter subscription form"""
    
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'autocomplete': 'email'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name (optional)',
                'autocomplete': 'name'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower().strip()
        
        # Check if already subscribed
        if NewsletterSubscriber.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError('This email is already subscribed.')
        
        return email


class QuickContactForm(forms.Form):
    """Simplified contact form for quick inquiries"""
    
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your Message',
            'rows': 4
        })
    )
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name.strip()) < 2:
            raise forms.ValidationError('Name must be at least 2 characters long.')
        return name.strip()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.lower().strip()
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message.strip()) < 10:
            raise forms.ValidationError('Message must be at least 10 characters long.')
        return message.strip()
