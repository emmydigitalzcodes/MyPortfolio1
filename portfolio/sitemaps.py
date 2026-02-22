from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from projects.models import Project
from blog.models import Post, Category


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = 'weekly'
    
    def items(self):
        return [
            'home:home',
            'home:about',
            'home:services',
            'home:resume',
            'home:testimonials',
            'home:skills',
            'projects:list',
            'projects:featured',
            'blog:list',
            'blog:featured',
            'contact:contact',
            'contact:faq',
        ]
    
    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    """Sitemap for project pages"""
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return Project.objects.filter(is_published=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return obj.get_absolute_url()


class BlogSitemap(Sitemap):
    """Sitemap for blog posts"""
    changefreq = 'weekly'
    priority = 0.8
    
    def items(self):
        return Post.objects.filter(status='published')
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    """Sitemap for blog categories"""
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return Category.objects.filter(is_active=True)
    
    def location(self, obj):
        return obj.get_absolute_url()
