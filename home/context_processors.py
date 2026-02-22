from django.conf import settings
from .models import PersonalInfo, SiteConfiguration
from contact.models import ContactInfo, SocialLink


def site_info(request):
    """Add site-wide information to context"""
    context = {
        # Site configuration from settings
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'Django Developer Portfolio'),
        'SITE_TAGLINE': getattr(settings, 'SITE_TAGLINE', ''),
        'SITE_DESCRIPTION': getattr(settings, 'SITE_DESCRIPTION', ''),
        'SITE_KEYWORDS': getattr(settings, 'SITE_KEYWORDS', ''),
        'SITE_AUTHOR': getattr(settings, 'SITE_AUTHOR', ''),
        'SITE_URL': getattr(settings, 'SITE_URL', ''),
        
        # Social links from settings
        'GITHUB_URL': getattr(settings, 'GITHUB_URL', ''),
        'LINKEDIN_URL': getattr(settings, 'LINKEDIN_URL', ''),
        'TWITTER_URL': getattr(settings, 'TWITTER_URL', ''),
        
        # Google Analytics
        'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', ''),
        
        # Debug mode
        'DEBUG': settings.DEBUG,
    }
    
    # Try to get from database models
    try:
        site_config = SiteConfiguration.get_solo()
        context['site_config'] = site_config
        context['SITE_NAME'] = site_config.site_name
        context['SITE_TAGLINE'] = site_config.site_tagline
        context['SITE_DESCRIPTION'] = site_config.site_description
        context['SITE_KEYWORDS'] = site_config.site_keywords
    except:
        pass
    
    try:
        personal_info = PersonalInfo.objects.first()
        context['personal_info'] = personal_info
    except:
        pass
    
    try:
        contact_info = ContactInfo.get_solo()
        context['contact_info'] = contact_info
    except:
        pass
    
    # Get active social links
    try:
        context['social_links'] = SocialLink.objects.filter(is_active=True)
    except:
        context['social_links'] = []
    
    return context
