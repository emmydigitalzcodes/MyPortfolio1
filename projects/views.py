from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Project, ProjectCategory, Technology


class ProjectListView(ListView):
    """Project list view with filtering"""
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Project.objects.filter(
            is_published=True
        ).select_related('category').prefetch_related('technologies', 'images')
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by technology
        tech_slug = self.request.GET.get('technology')
        if tech_slug:
            queryset = queryset.filter(technologies__slug=tech_slug)
        
        # Search
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(technologies__name__icontains=search_query)
            ).distinct()
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all categories for filter
        context['categories'] = ProjectCategory.objects.filter(is_active=True)
        
        # Get all technologies for filter
        context['technologies'] = Technology.objects.filter(is_active=True)
        
        # Get featured projects
        context['featured_projects'] = Project.objects.filter(
            is_published=True,
            featured__gt=0
        ).select_related('category').prefetch_related('technologies')[:3]
        
        # Current filters
        context['current_category'] = self.request.GET.get('category', '')
        context['current_technology'] = self.request.GET.get('technology', '')
        context['search_query'] = self.request.GET.get('q', '')
        
        # Project stats
        context['total_projects'] = Project.objects.filter(is_published=True).count()
        context['featured_count'] = Project.objects.filter(
            is_published=True, featured__gt=0
        ).count()
        
        return context


class ProjectDetailView(DetailView):
    """Project detail view"""
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Project.objects.filter(
            is_published=True
        ).select_related('category').prefetch_related(
            'technologies', 'images', 'stats'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        # Get related projects
        related_projects = Project.objects.filter(
            is_published=True
        ).exclude(id=project.id)
        
        # Prioritize same category
        if project.category:
            related_projects = related_projects.filter(
                category=project.category
            ) | related_projects
        
        # Then prioritize same technologies
        if project.technologies.exists():
            related_projects = related_projects.filter(
                technologies__in=project.technologies.all()
            ) | related_projects
        
        context['related_projects'] = related_projects.distinct()[:3]
        
        # Get next and previous projects
        context['next_project'] = Project.objects.filter(
            is_published=True,
            created_at__gt=project.created_at
        ).order_by('created_at').first()
        
        context['previous_project'] = Project.objects.filter(
            is_published=True,
            created_at__lt=project.created_at
        ).order_by('-created_at').first()
        
        return context


class ProjectCategoryView(ListView):
    """View projects by category"""
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 9
    
    def get_queryset(self):
        self.category = get_object_or_404(
            ProjectCategory,
            slug=self.kwargs['slug'],
            is_active=True
        )
        return Project.objects.filter(
            category=self.category,
            is_published=True
        ).select_related('category').prefetch_related('technologies')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = ProjectCategory.objects.filter(is_active=True)
        context['technologies'] = Technology.objects.filter(is_active=True)
        context['page_title'] = f"Projects in {self.category.name}"
        return context


class TechnologyView(ListView):
    """View projects by technology"""
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 9
    
    def get_queryset(self):
        self.technology = get_object_or_404(
            Technology,
            slug=self.kwargs['slug'],
            is_active=True
        )
        return Project.objects.filter(
            technologies=self.technology,
            is_published=True
        ).select_related('category').prefetch_related('technologies')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['technology'] = self.technology
        context['categories'] = ProjectCategory.objects.filter(is_active=True)
        context['technologies'] = Technology.objects.filter(is_active=True)
        context['page_title'] = f"Projects using {self.technology.name}"
        return context


class FeaturedProjectsView(ListView):
    """View featured projects"""
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 9
    
    def get_queryset(self):
        return Project.objects.filter(
            is_published=True,
            featured__gt=0
        ).select_related('category').prefetch_related('technologies')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProjectCategory.objects.filter(is_active=True)
        context['technologies'] = Technology.objects.filter(is_active=True)
        context['page_title'] = "Featured Projects"
        context['showing_featured'] = True
        return context


def project_search(request):
    """AJAX search for projects"""
    query = request.GET.get('q', '')
    
    projects = []
    if query:
        projects_list = Project.objects.filter(
            is_published=True
        ).filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )[:5]
        
        projects = [{
            'title': p.title,
            'slug': p.slug,
            'thumbnail': p.thumbnail.url if p.thumbnail else None,
            'description': p.description[:100] + '...' if len(p.description) > 100 else p.description,
        } for p in projects_list]
    
    return render(request, 'projects/partials/search_results.html', {
        'projects': projects,
        'query': query
    })
