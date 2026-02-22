from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Category, Tag, Post, Comment, NewsletterSubscriber


class PostListView(ListView):
    """Blog post list view"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Post.objects.filter(
            status='published'
        ).select_related('category', 'author').prefetch_related('tags')
        
        # Search
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(excerpt__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get categories
        context['categories'] = Category.objects.filter(is_active=True)
        
        # Get popular tags
        context['tags'] = Tag.objects.filter(is_active=True)[:15]
        
        # Get featured posts
        context['featured_posts'] = Post.objects.filter(
            status='published',
            is_featured=True
        ).select_related('category')[:3]
        
        # Recent posts for sidebar
        context['recent_posts'] = Post.objects.filter(
            status='published'
        ).exclude(
            id__in=[p.id for p in context['featured_posts']]
        )[:5]
        
        # Search query
        context['search_query'] = self.request.GET.get('q', '')
        
        return context


class PostDetailView(DetailView):
    """Blog post detail view"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Post.objects.filter(
            status='published'
        ).select_related('category', 'author').prefetch_related('tags', 'comments')
    
    def get(self, request, *args, **kwargs):
        # Increment view count
        response = super().get(request, *args, **kwargs)
        post = self.get_object()
        post.views_count += 1
        post.save(update_fields=['views_count'])
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Get related posts
        context['related_posts'] = post.related_posts[:3]
        
        # Get categories for sidebar
        context['categories'] = Category.objects.filter(is_active=True)
        
        # Get popular tags
        context['tags'] = Tag.objects.filter(is_active=True)[:15]
        
        # Recent posts for sidebar
        context['recent_posts'] = Post.objects.filter(
            status='published'
        ).exclude(id=post.id)[:5]
        
        # Approved comments
        context['comments'] = post.comments.filter(
            is_approved=True,
            parent=None
        ).prefetch_related('replies')
        
        # Comment form
        context['comment_form'] = None  # Will be added if implementing comments
        
        # Next and previous posts
        context['next_post'] = Post.objects.filter(
            status='published',
            published_at__gt=post.published_at
        ).order_by('published_at').first()
        
        context['previous_post'] = Post.objects.filter(
            status='published',
            published_at__lt=post.published_at
        ).order_by('-published_at').first()
        
        return context


class CategoryView(ListView):
    """View posts by category"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['slug'],
            is_active=True
        )
        return Post.objects.filter(
            category=self.category,
            status='published'
        ).select_related('category', 'author').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.filter(is_active=True)
        context['tags'] = Tag.objects.filter(is_active=True)[:15]
        context['page_title'] = f"Posts in {self.category.name}"
        return context


class TagView(ListView):
    """View posts by tag"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        self.tag = get_object_or_404(
            Tag,
            slug=self.kwargs['slug'],
            is_active=True
        )
        return Post.objects.filter(
            tags=self.tag,
            status='published'
        ).select_related('category', 'author').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['categories'] = Category.objects.filter(is_active=True)
        context['tags'] = Tag.objects.filter(is_active=True)[:15]
        context['page_title'] = f"Posts tagged with #{self.tag.name}"
        return context


class FeaturedPostsView(ListView):
    """View featured posts"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        return Post.objects.filter(
            status='published',
            is_featured=True
        ).select_related('category', 'author').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['tags'] = Tag.objects.filter(is_active=True)[:15]
        context['page_title'] = "Featured Articles"
        context['showing_featured'] = True
        return context


def newsletter_subscribe(request):
    """Handle newsletter subscription"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        name = request.POST.get('name', '').strip()
        
        if email:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'name': name, 'is_active': True}
            )
            
            if not created:
                if subscriber.is_active:
                    return render(request, 'blog/partials/newsletter_message.html', {
                        'message': 'You are already subscribed!',
                        'message_type': 'info'
                    })
                else:
                    subscriber.is_active = True
                    subscriber.name = name or subscriber.name
                    subscriber.save()
            
            return render(request, 'blog/partials/newsletter_message.html', {
                'message': 'Thank you for subscribing!',
                'message_type': 'success'
            })
        
        return render(request, 'blog/partials/newsletter_message.html', {
            'message': 'Please enter a valid email address.',
            'message_type': 'error'
        })
    
    return redirect('blog:list')


def post_search(request):
    """AJAX search for posts"""
    query = request.GET.get('q', '')
    
    posts = []
    if query:
        posts_list = Post.objects.filter(
            status='published'
        ).filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query)
        )[:5]
        
        posts = [{
            'title': p.title,
            'slug': p.slug,
            'featured_image': p.featured_image.url if p.featured_image else None,
            'excerpt': p.excerpt[:100] + '...' if len(p.excerpt) > 100 else p.excerpt,
            'category': p.category.name if p.category else None,
        } for p in posts_list]
    
    return render(request, 'blog/partials/search_results.html', {
        'posts': posts,
        'query': query
    })
