from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class SkillCategory(models.Model):
    """Category for organizing skills (e.g., Frontend, Backend, Database)"""
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Skill Categories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Skill(models.Model):
    """Technical skills with proficiency levels"""
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    proficiency = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Proficiency level from 0 to 100"
    )
    icon_class = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Font Awesome or Bootstrap icon class (e.g., 'fab fa-python')"
    )
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-proficiency', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.proficiency}%)"


class Experience(models.Model):
    """Work experience entries"""
    EMPLOYMENT_TYPES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
    ]
    
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES, default='full_time')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave blank for current position")
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    achievements = models.TextField(blank=True, help_text="Key achievements (one per line)")
    technologies = models.CharField(max_length=500, blank=True, help_text="Comma-separated list of technologies used")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-is_current', '-start_date', 'order']
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    @property
    def duration(self):
        """Calculate duration of employment"""
        from datetime import date
        end = self.end_date if self.end_date else date.today()
        months = (end.year - self.start_date.year) * 12 + (end.month - self.start_date.month)
        years = months // 12
        remaining_months = months % 12
        
        if years > 0 and remaining_months > 0:
            return f"{years} yr {remaining_months} mos"
        elif years > 0:
            return f"{years} yr"
        else:
            return f"{remaining_months} mos"


class Education(models.Model):
    """Education entries"""
    DEGREE_TYPES = [
        ('high_school', 'High School'),
        ('associate', 'Associate Degree'),
        ('bachelor', "Bachelor's Degree"),
        ('master', "Master's Degree"),
        ('doctorate', 'Doctorate'),
        ('certificate', 'Certificate'),
        ('bootcamp', 'Bootcamp'),
    ]
    
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    degree_type = models.CharField(max_length=20, choices=DEGREE_TYPES, default='bachelor')
    field_of_study = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    gpa = models.CharField(max_length=10, blank=True)
    logo = models.ImageField(upload_to='education/', blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Education"
        ordering = ['-end_date', '-start_date', 'order']
    
    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Certification(models.Model):
    """Professional certifications"""
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=200, blank=True)
    credential_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to='certifications/', blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-issue_date', 'order']
    
    def __str__(self):
        return f"{self.name} - {self.issuing_organization}"


class Testimonial(models.Model):
    """Client/employer testimonials"""
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    photo = models.ImageField(upload_to='testimonials/', blank=True)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"Testimonial from {self.name}"


class Service(models.Model):
    """Services offered"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_class = models.CharField(
        max_length=100,
        default='fas fa-code',
        help_text="Font Awesome icon class"
    )
    features = models.TextField(blank=True, help_text="List of features (one per line)")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    @property
    def features_list(self):
        """Return features as a list"""
        return [f.strip() for f in self.features.split('\n') if f.strip()]


class PersonalInfo(models.Model):
    """Personal information for the portfolio owner"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=200, help_text="Professional title (e.g., 'Senior Django Developer')")
    tagline = models.CharField(max_length=300, blank=True)
    bio = models.TextField(help_text="Short bio for about section")
    about_me = models.TextField(help_text="Detailed about me content")
    profile_photo = models.ImageField(upload_to='profile/', blank=True)
    resume = models.FileField(upload_to='resume/', blank=True, help_text="PDF resume file")
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    stackoverflow = models.URLField(blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    projects_completed = models.PositiveIntegerField(default=0)
    happy_clients = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Personal Info"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class SiteConfiguration(models.Model):
    """Global site configuration"""
    site_name = models.CharField(max_length=200, default="Django Developer Portfolio")
    site_tagline = models.CharField(max_length=300, blank=True)
    site_description = models.TextField(blank=True)
    site_keywords = models.TextField(blank=True, help_text="Comma-separated keywords for SEO")
    favicon = models.ImageField(upload_to='site/', blank=True)
    logo = models.ImageField(upload_to='site/', blank=True)
    footer_text = models.TextField(blank=True)
    enable_dark_mode = models.BooleanField(default=True)
    enable_blog = models.BooleanField(default=True)
    enable_contact_form = models.BooleanField(default=True)
    enable_testimonials = models.BooleanField(default=True)
    google_analytics_id = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name_plural = "Site Configuration"
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteConfiguration.objects.exists():
            raise ValueError("Only one SiteConfiguration instance is allowed")
        super().save(*args, **kwargs)
    
    @classmethod
    def get_solo(cls):
        """Get or create the singleton instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
