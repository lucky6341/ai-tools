from django.contrib import admin
from django.db.models import Count
from .models import AITool, Category, ToolComparison
import joblib
from .utils import ToolRecommender

@admin.action(description='Mark selected as featured')
def make_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)

@admin.action(description='Remove featured status')
def remove_featured(modeladmin, request, queryset):
    queryset.update(is_featured=False)

@admin.action(description='Increase ad priority')
def increase_ad_priority(modeladmin, request, queryset):
    for obj in queryset:
        obj.ad_priority += 1
        obj.save()

@admin.action(description='Decrease ad priority')
def decrease_ad_priority(modeladmin, request, queryset):
    for obj in queryset:
        if obj.ad_priority > 0:
            obj.ad_priority -= 1
            obj.save()

@admin.action(description='Verify selected tools')
def verify_tools(modeladmin, request, queryset):
    queryset.update(verification_status='VER')

@admin.action(description='Retrain recommendation model')
def retrain_recommender(modeladmin, request, queryset):
    recommender = ToolRecommender()
    success = recommender.train_model()
    if success:
        modeladmin.message_user(request, "Recommendation model retrained successfully")
    else:
        modeladmin.message_user(request, "Failed to retrain model", level='error')

@admin.action(description='Generate comparison data')
def generate_comparison(modeladmin, request, queryset):
    if queryset.count() < 2:
        modeladmin.message_user(request, "Select at least 2 tools for comparison", level='error')
        return
    
    comparison = ToolComparison()
    comparison.title = f"Comparison of {', '.join([t.name for t in queryset])}"
    comparison.save()
    comparison.tools.set(queryset)
    
    from .utils import generate_comparison_matrix
    comparison.comparison_data = generate_comparison_matrix(queryset)
    comparison.save()
    
    modeladmin.message_user(request, f"Comparison '{comparison.title}' created successfully")

def attach_admin_actions():
    """Attach actions to admin models"""
    AIToolAdmin = admin.site._registry[AITool].__class__
    ToolComparisonAdmin = admin.site._registry[ToolComparison].__class__
    
    # Add actions to AIToolAdmin
    AIToolAdmin.actions = [
        make_featured, 
        remove_featured, 
        increase_ad_priority, 
        decrease_ad_priority,
        verify_tools,
        generate_comparison,
        retrain_recommender
    ]
    
    # Add action to ToolComparisonAdmin
    ToolComparisonAdmin.actions = [generate_comparison]