from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import (
    SkillCategory, Skill, Experience, Education, 
    Certification, Testimonial, Service, PersonalInfo
)
from projects.models import Project, Technology
from blog.models import Post


class HomeView(TemplateView):
    """Home page view with all sections"""
    template_name = 'home/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get personal info
        try:
            context['personal_info'] = PersonalInfo.objects.first()
        except:
            context['personal_info'] = None
        
        # Get featured projects (limit to 6)
        context['featured_projects'] = Project.objects.filter(
            is_published=True,
            featured__gt=0
        ).select_related('category').prefetch_related('technologies')[:6]
        
        # Get skills organized by category
        context['skill_categories'] = SkillCategory.objects.filter(
            is_active=True
        ).prefetch_related('skills')
        
        # Get all active skills
        context['skills'] = Skill.objects.filter(
            is_active=True
        ).select_related('category')
        
        # Get experience
        context['experiences'] = Experience.objects.filter(
            is_active=True
        )[:5]
        
        # Get education
        context['educations'] = Education.objects.filter(
            is_active=True
        )[:3]
        
        # Get testimonials
        context['testimonials'] = Testimonial.objects.filter(
            is_active=True
        )[:6]
        
        # Get services
        context['services'] = Service.objects.filter(
            is_active=True
        )
        
        # Get recent blog posts
        context['recent_posts'] = Post.objects.filter(
            status='published'
        ).select_related('category', 'author').prefetch_related('tags')[:3]
        
        # Get technologies for skills display
        context['technologies'] = Technology.objects.filter(
            is_active=True
        )[:12]
        
        return context


class AboutView(TemplateView):
    """About page view"""
    template_name = 'home/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get personal info
        try:
            context['personal_info'] = PersonalInfo.objects.first()
        except:
            context['personal_info'] = None
        
        # Get all skills
        context['skill_categories'] = SkillCategory.objects.filter(
            is_active=True
        ).prefetch_related('skills')
        
        # Get all experience
        context['experiences'] = Experience.objects.filter(
            is_active=True
        )
        
        # Get all education
        context['educations'] = Education.objects.filter(
            is_active=True
        )
        
        # Get certifications
        context['certifications'] = Certification.objects.filter(
            is_active=True
        )
        
        # Get testimonials
        context['testimonials'] = Testimonial.objects.filter(
            is_active=True
        )
        
        # Get stats
        context['stats'] = {
            'years_experience': self.get_years_experience(),
            'projects_completed': Project.objects.filter(is_published=True).count(),
            'technologies_count': Technology.objects.filter(is_active=True).count(),
            'happy_clients': getattr(context.get('personal_info'), 'happy_clients', 0) if context.get('personal_info') else 0,
        }
        
        return context
    
    def get_years_experience(self):
        """Calculate total years of experience"""
        try:
            personal_info = PersonalInfo.objects.first()
            if personal_info:
                return personal_info.years_of_experience
        except:
            pass
        
        # Calculate from experience entries
        from datetime import date
        earliest = Experience.objects.filter(
            is_active=True
        ).order_by('start_date').first()
        
        if earliest:
            years = (date.today() - earliest.start_date).days // 365
            return years
        
        return 0


class ServicesView(TemplateView):
    """Services page view"""
    template_name = 'home/services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_active=True)
        return context


class ResumeView(TemplateView):
    """Resume download/view page"""
    template_name = 'home/resume.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            context['personal_info'] = PersonalInfo.objects.first()
        except:
            context['personal_info'] = None
        
        context['experiences'] = Experience.objects.filter(is_active=True)
        context['educations'] = Education.objects.filter(is_active=True)
        context['certifications'] = Certification.objects.filter(is_active=True)
        context['skills'] = Skill.objects.filter(is_active=True).select_related('category')
        
        return context


class TestimonialsView(ListView):
    """Testimonials page view"""
    model = Testimonial
    template_name = 'home/testimonials.html'
    context_object_name = 'testimonials'
    paginate_by = 9
    
    def get_queryset(self):
        return Testimonial.objects.filter(is_active=True)


class SkillsView(TemplateView):
    """Skills page view"""
    template_name = 'home/skills.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skill_categories'] = SkillCategory.objects.filter(
            is_active=True
        ).prefetch_related('skills')
        context['technologies'] = Technology.objects.filter(is_active=True)
        return context


def custom_404_view(request, exception=None):
    """Custom 404 error page"""
    return render(request, 'errors/404.html', status=404)


def custom_500_view(request):
    """Custom 500 error page"""
    return render(request, 'errors/500.html', status=500)
