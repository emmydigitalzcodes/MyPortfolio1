from django.contrib import admin
from .models import Technology, ProjectCategory, Project, ProjectImage, ProjectStat


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'is_active']
    list_editable = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'caption', 'order', 'is_featured']


class ProjectStatInline(admin.TabularInline):
    model = ProjectStat
    extra = 1
    fields = ['label', 'value', 'icon_class', 'order']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status', 'featured', 
        'is_published', 'created_at', 'updated_at'
    ]
    list_filter = [
        'status', 'is_published', 'featured', 
        'category', 'technologies', 'created_at'
    ]
    list_editable = ['status', 'featured', 'is_published']
    search_fields = ['title', 'description', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    filter_horizontal = ['technologies']
    inlines = [ProjectImageInline, ProjectStatInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'subtitle', 'description', 'content')
        }),
        ('Status & Visibility', {
            'fields': ('status', 'is_published', 'featured')
        }),
        ('Categorization', {
            'fields': ('category', 'technologies')
        }),
        ('URLs', {
            'fields': ('live_url', 'github_url', 'documentation_url')
        }),
        ('Media', {
            'fields': ('thumbnail',)
        }),
        ('Project Details', {
            'fields': ('client_name', 'project_date', 'completion_date', 'duration')
        }),
        ('Technical Information', {
            'fields': ('challenges', 'solutions', 'architecture', 'key_features'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_published', 'make_draft', 'make_featured']
    
    def make_published(self, request, queryset):
        queryset.update(status='published', is_published=True)
    make_published.short_description = "Mark selected projects as published"
    
    def make_draft(self, request, queryset):
        queryset.update(status='draft', is_published=False)
    make_draft.short_description = "Mark selected projects as draft"
    
    def make_featured(self, request, queryset):
        queryset.update(featured=1)
    make_featured.short_description = "Mark selected projects as featured"


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ['project', 'caption', 'order', 'is_featured']
    list_filter = ['is_featured', 'project']
    list_editable = ['order', 'is_featured']
    search_fields = ['project__title', 'caption']


@admin.register(ProjectStat)
class ProjectStatAdmin(admin.ModelAdmin):
    list_display = ['project', 'label', 'value', 'order']
    list_filter = ['project']
    list_editable = ['order']
    search_fields = ['project__title', 'label']
