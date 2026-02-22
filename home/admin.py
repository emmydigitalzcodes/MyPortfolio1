from django.contrib import admin
from .models import (
    SkillCategory, Skill, Experience, Education, 
    Certification, Testimonial, Service, PersonalInfo, SiteConfiguration
)


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'is_active']
    list_filter = ['category', 'is_active']
    list_editable = ['is_active']
    search_fields = ['name']
    ordering = ['-proficiency']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'employment_type', 'start_date', 'end_date', 'is_current', 'is_active']
    list_filter = ['employment_type', 'is_current', 'is_active']
    list_editable = ['is_active']
    search_fields = ['title', 'company', 'description']
    date_hierarchy = 'start_date'
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'company', 'location', 'employment_type')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Details', {
            'fields': ('description', 'achievements', 'technologies')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'field_of_study', 'start_date', 'end_date', 'is_active']
    list_filter = ['degree_type', 'is_active']
    list_editable = ['is_active']
    search_fields = ['institution', 'degree', 'field_of_study']
    date_hierarchy = 'start_date'


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'issuing_organization', 'issue_date', 'expiration_date', 'is_active']
    list_filter = ['is_active']
    list_editable = ['is_active']
    search_fields = ['name', 'issuing_organization']
    date_hierarchy = 'issue_date'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'company', 'rating', 'is_active', 'created_at']
    list_filter = ['rating', 'is_active']
    list_editable = ['is_active']
    search_fields = ['name', 'content']
    readonly_fields = ['created_at']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'description']


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'title', 'email', 'years_of_experience']
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'title', 'tagline', 'profile_photo')
        }),
        ('About', {
            'fields': ('bio', 'about_me')
        }),
        ('Contact', {
            'fields': ('email', 'phone', 'location', 'website')
        }),
        ('Social Links', {
            'fields': ('github', 'linkedin', 'twitter', 'stackoverflow')
        }),
        ('Stats', {
            'fields': ('years_of_experience', 'projects_completed', 'happy_clients')
        }),
        ('Resume', {
            'fields': ('resume',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'enable_blog', 'enable_contact_form', 'enable_dark_mode']
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'site_tagline', 'site_description', 'site_keywords')
        }),
        ('Branding', {
            'fields': ('favicon', 'logo')
        }),
        ('Features', {
            'fields': ('enable_dark_mode', 'enable_blog', 'enable_contact_form', 'enable_testimonials')
        }),
        ('Integrations', {
            'fields': ('google_analytics_id',)
        }),
        ('Footer', {
            'fields': ('footer_text',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
