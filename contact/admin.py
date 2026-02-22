from django.contrib import admin
from .models import ContactMessage, ContactInfo, FAQ, SocialLink


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'email', 'subject', 'reason', 
        'status', 'is_important', 'created_at'
    ]
    list_filter = [
        'status', 'reason', 'is_important', 
        'created_at', 'recaptcha_score'
    ]
    list_editable = ['status', 'is_important']
    search_fields = ['name', 'email', 'subject', 'message']
    date_hierarchy = 'created_at'
    readonly_fields = [
        'ip_address', 'user_agent', 'referrer', 
        'recaptcha_score', 'created_at', 'updated_at', 'replied_at'
    ]
    
    fieldsets = (
        ('Sender Information', {
            'fields': ('name', 'email', 'phone', 'company')
        }),
        ('Message', {
            'fields': ('subject', 'message', 'reason')
        }),
        ('Status', {
            'fields': ('status', 'is_important')
        }),
        ('Security', {
            'fields': ('recaptcha_score',),
            'classes': ('collapse',)
        }),
        ('Meta', {
            'fields': ('ip_address', 'user_agent', 'referrer'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'replied_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = [
        'mark_as_read', 'mark_as_replied', 
        'mark_as_spam', 'mark_as_archived',
        'mark_as_important', 'mark_as_not_important'
    ]
    
    def mark_as_read(self, request, queryset):
        queryset.update(status='read')
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_replied(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='replied', replied_at=timezone.now())
    mark_as_replied.short_description = "Mark selected messages as replied"
    
    def mark_as_spam(self, request, queryset):
        queryset.update(status='spam')
    mark_as_spam.short_description = "Mark selected messages as spam"
    
    def mark_as_archived(self, request, queryset):
        queryset.update(status='archived')
    mark_as_archived.short_description = "Mark selected messages as archived"
    
    def mark_as_important(self, request, queryset):
        queryset.update(is_important=True)
    mark_as_important.short_description = "Mark selected messages as important"
    
    def mark_as_not_important(self, request, queryset):
        queryset.update(is_important=False)
    mark_as_not_important.short_description = "Mark selected messages as not important"


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Contact Details', {
            'fields': ('email', 'phone', 'phone_secondary')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'zip_code', 'country')
        }),
        ('Working Hours', {
            'fields': ('working_hours',)
        }),
        ('Social Links', {
            'fields': (
                'github_url', 'linkedin_url', 'twitter_url',
                'facebook_url', 'instagram_url', 'youtube_url',
                'stackoverflow_url'
            )
        }),
        ('Map', {
            'fields': ('map_embed_url',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['question', 'answer']


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'name', 'url', 'order', 'is_active']
    list_filter = ['platform', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'url']
