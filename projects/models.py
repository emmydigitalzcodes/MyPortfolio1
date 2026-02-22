from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Technology(models.Model):
    """Technologies used in projects"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    icon_class = models.CharField(
        max_length=100,
        blank=True,
        help_text="Font Awesome or Devicon class (e.g., 'fab fa-python')"
    )
    color = models.CharField(
        max_length=7,
        default='#6c757d',
        help_text="Hex color code for the technology badge"
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class ProjectCategory(models.Model):
    """Categories for organizing projects"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Project Categories"
        ordering = ['order', 'name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """Portfolio projects"""
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('planned', 'Planned'),
    ]
    
    FEATURED_CHOICES = [
        (0, 'Not Featured'),
        (1, 'Featured'),
        (2, 'Main Featured'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(help_text="Brief description for project cards")
    content = models.TextField(help_text="Detailed description for project detail page")
    
    # Project status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    is_published = models.BooleanField(default=True)
    featured = models.IntegerField(choices=FEATURED_CHOICES, default=0)
    
    # Relationships
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects'
    )
    technologies = models.ManyToManyField(Technology, related_name='projects', blank=True)
    
    # URLs
    live_url = models.URLField(blank=True, help_text="Link to live demo")
    github_url = models.URLField(blank=True, help_text="Link to GitHub repository")
    documentation_url = models.URLField(blank=True)
    
    # Media
    thumbnail = models.ImageField(
        upload_to='projects/thumbnails/',
        help_text="Main project image for cards"
    )
    
    # Meta
    client_name = models.CharField(max_length=200, blank=True)
    project_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    duration = models.CharField(max_length=100, blank=True, help_text="e.g., '3 months'")
    
    # Technical details
    challenges = models.TextField(blank=True, help_text="Challenges faced during development")
    solutions = models.TextField(blank=True, help_text="Solutions implemented")
    architecture = models.TextField(blank=True, help_text="Technical architecture description")
    key_features = models.TextField(blank=True, help_text="Key features (one per line)")
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-featured', '-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'slug': self.slug})
    
    @property
    def key_features_list(self):
        """Return key features as a list"""
        return [f.strip() for f in self.key_features.split('\n') if f.strip()]
    
    @property
    def is_featured(self):
        return self.featured > 0
    
    @property
    def display_title(self):
        return self.meta_title or self.title


class ProjectImage(models.Model):
    """Additional images for projects"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order', '-is_featured']
    
    def __str__(self):
        return f"Image for {self.project.title}"


class ProjectStat(models.Model):
    """Statistics/metrics for projects"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='stats')
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Project Stats"
    
    def __str__(self):
        return f"{self.label}: {self.value}"
