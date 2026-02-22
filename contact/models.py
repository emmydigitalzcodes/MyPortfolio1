from django.db import models
from django.core.validators import EmailValidator


class ContactMessage(models.Model):
    """Contact form messages"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('spam', 'Spam'),
        ('archived', 'Archived'),
    ]
    
    REASON_CHOICES = [
        ('general', 'General Inquiry'),
        ('project', 'Project Collaboration'),
        ('job', 'Job Opportunity'),
        ('consulting', 'Consulting'),
        ('feedback', 'Feedback'),
        ('other', 'Other'),
    ]
    
    # Sender info
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    company = models.CharField(max_length=200, blank=True)
    
    # Message details
    subject = models.CharField(max_length=200)
    message = models.TextField()
    reason = models.CharField(
        max_length=20,
        choices=REASON_CHOICES,
        default='general'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    is_important = models.BooleanField(default=False)
    
    # reCAPTCHA
    recaptcha_score = models.FloatField(null=True, blank=True)
    
    # Meta
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-is_important', '-created_at']
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
    
    @property
    def is_new(self):
        return self.status == 'new'
    
    @property
    def preview(self):
        """Return a preview of the message"""
        return self.message[:100] + '...' if len(self.message) > 100 else self.message


class ContactInfo(models.Model):
    """Contact information displayed on the site"""
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    phone_secondary = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Working hours
    working_hours = models.TextField(
        blank=True,
        help_text="e.g., 'Mon-Fri: 9AM - 6PM'"
    )
    
    # Social links
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    stackoverflow_url = models.URLField(blank=True)
    
    # Map
    map_embed_url = models.URLField(
        blank=True,
        help_text="Google Maps embed URL"
    )
    
    class Meta:
        verbose_name_plural = "Contact Info"
    
    def __str__(self):
        return "Contact Information"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and ContactInfo.objects.exists():
            raise ValueError("Only one ContactInfo instance is allowed")
        super().save(*args, **kwargs)
    
    @classmethod
    def get_solo(cls):
        """Get or create the singleton instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class FAQ(models.Model):
    """Frequently Asked Questions"""
    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "FAQs"
        ordering = ['order', 'question']
    
    def __str__(self):
        return self.question


class SocialLink(models.Model):
    """Social media links"""
    PLATFORM_CHOICES = [
        ('github', 'GitHub'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('stackoverflow', 'Stack Overflow'),
        ('medium', 'Medium'),
        ('dev', 'Dev.to'),
        ('dribbble', 'Dribbble'),
        ('behance', 'Behance'),
        ('other', 'Other'),
    ]
    
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    name = models.CharField(max_length=100, blank=True)
    url = models.URLField()
    icon_class = models.CharField(
        max_length=100,
        blank=True,
        help_text="Custom icon class (optional)"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'platform']
    
    def __str__(self):
        return self.name or self.get_platform_display()
    
    @property
    def default_icon(self):
        """Return default icon class based on platform"""
        icons = {
            'github': 'fab fa-github',
            'linkedin': 'fab fa-linkedin-in',
            'twitter': 'fab fa-twitter',
            'facebook': 'fab fa-facebook-f',
            'instagram': 'fab fa-instagram',
            'youtube': 'fab fa-youtube',
            'stackoverflow': 'fab fa-stack-overflow',
            'medium': 'fab fa-medium-m',
            'dev': 'fab fa-dev',
            'dribbble': 'fab fa-dribbble',
            'behance': 'fab fa-behance',
            'other': 'fas fa-link',
        }
        return icons.get(self.platform, 'fas fa-link')
    
    @property
    def display_icon(self):
        return self.icon_class or self.default_icon
