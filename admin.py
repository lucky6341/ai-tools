from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import AITool, Category, ToolComparison, ToolSubmission, AdPlacement

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'icon': forms.TextInput(attrs={'placeholder': 'fas fa-robot'})
        }

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ('name', 'slug', 'parent', 'tool_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    
    def tool_count(self, obj):
        return obj.tool_count
    tool_count.short_description = "Tools"

@admin.register(AITool)
class AIToolAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'website_link', 
        'pricing_type', 
        'is_featured',
        'last_verified',
        'view_count'
    )
    list_filter = ('pricing_type', 'is_featured', 'categories', 'last_verified')
    search_fields = ('name', 'short_description', 'description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('categories',)
    readonly_fields = ('created', 'updated', 'view_count')
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'website', 'logo', 'short_description', 'description')
        }),
        ('Categorization', {
            'fields': ('categories',)
        }),
        ('Pricing & Technical', {
            'fields': (
                'pricing_type', 
                'price_range', 
                'api_available', 
                'open_source',
                'deployment_options',
                'technical_complexity',
                'use_case_matrix'
            )
        }),
        ('Promotion', {
            'fields': ('affiliate_link', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('view_count', 'popularity_score', 'last_verified')
        }),
        ('Metadata', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )
    
    def website_link(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.website, obj.website)
    website_link.short_description = "Website"

@admin.register(ToolComparison)
class ToolComparisonAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created', 'updated', 'view_count', 'tools_count')
    filter_horizontal = ('tools',)
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created', 'updated', 'view_count')
    
    def tools_count(self, obj):
        return obj.tools.count()
    tools_count.short_description = "Tools"

@admin.register(ToolSubmission)
class ToolSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'submitter_name', 'submitted_at', 'status')
    list_filter = ('status', 'submitted_at')
    search_fields = ('name', 'website', 'submitter_name')
    readonly_fields = ('submitted_at',)
    fieldsets = (
        ('Tool Information', {
            'fields': ('name', 'website', 'description', 'categories', 'pricing_type')
        }),
        ('Submitter Information', {
            'fields': ('submitter_name', 'submitter_email')
        }),
        ('Review Status', {
            'fields': ('status', 'notes')
        }),
        ('Metadata', {
            'fields': ('submitted_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(AdPlacement)
class AdPlacementAdmin(admin.ModelAdmin):
    list_display = ('name', 'placement_type', 'base_price', 'is_active')
    list_editable = ('base_price', 'is_active')
    ordering = ('placement_type',)
    
    def save_model(self, request, obj, form, change):
        if not obj.code_snippet:
            if obj.placement_type == 'HERO':
                obj.code_snippet = f'<div class="ad-hero" data-ad-type="hero" data-ad-id="{obj.id}"></div>'
            elif obj.placement_type == 'SIDEBAR':
                obj.code_snippet = f'<div class="ad-sidebar" data-ad-type="sidebar" data-ad-id="{obj.id}"></div>'
        super().save_model(request, obj, form, change)