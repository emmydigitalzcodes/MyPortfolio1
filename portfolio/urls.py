"""
URL configuration for portfolio project.
"""
from django.contrib import admin
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

urlpatterns = [
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
    
    # Debug toolbar (optional)
    # urlpatterns = [path('__debug__/', include('debug_toolbar.urls'))] + urlpatterns

# Custom error handlers
handler404 = 'home.views.custom_404_view'
handler500 = 'home.views.custom_500_view'
