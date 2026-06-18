"""
URL configuration for portfolio project.
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from .sitemaps import (
    StaticViewSitemap, ProjectSitemap,
    BlogSitemap, CategorySitemap
)

# Sitemap configuration
sitemaps = {
    'static': StaticViewSitemap,
    'projects': ProjectSitemap,
    'blog': BlogSitemap,
    'categories': CategorySitemap,
}


def health(request):
    return HttpResponse("OK")


    """Temporary test endpoint - remove after confirming email works"""
    try:
        import resend
        resend.api_key = settings.RESEND_API_KEY
        email = resend.Emails.send({
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [settings.CONTACT_EMAIL],
            "subject": "Test from Railway",
            "text": "Resend is working on Railway! Your contact form emails will now be delivered."
        })
        return HttpResponse(f"Email sent successfully! Resend ID: {email['id']} — Check your inbox at {settings.CONTACT_EMAIL}")
    except Exception as e:
        return HttpResponse(f"Email failed: {str(e)}")


urlpatterns = [
    path('health/', health),

    # Admin
    path('admin/', admin.site.urls),

    # Home app
    path('', include('home.urls', namespace='home')),

    # Projects app
    path('projects/', include('projects.urls', namespace='projects')),

    # Blog app
    path('blog/', include('blog.urls', namespace='blog')),

    # Contact app
    path('contact/', include('contact.urls', namespace='contact')),

    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

    # Robots.txt
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain'
    )),

    # Humans.txt
    path('humans.txt', TemplateView.as_view(
        template_name='humans.txt',
        content_type='text/plain'
    )),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler404 = 'home.views.custom_404_view'
handler500 = 'home.views.custom_500_view'