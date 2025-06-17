from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import AITool, Category, ToolComparison

@receiver(post_save, sender=AITool)
@receiver(post_delete, sender=AITool)
def update_tool_cache(sender, instance, **kwargs):
    cache.delete_many([
        'featured_tools',
        'popular_tools',
        'category_tools'
    ])
    # Clear recommendation caches
    for tool in AITool.objects.all():
        cache.delete(f"tool_recs_{tool.id}")

@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def update_category_cache(sender, instance, **kwargs):
    cache.delete('category_tree')
    cache.delete('all_categories')

@receiver(post_save, sender=ToolComparison)
@receiver(post_delete, sender=ToolComparison)
def update_comparison_cache(sender, instance, **kwargs):
    cache.delete('featured_comparisons')
    for tool in instance.tools.all():
        cache.delete(f"tool_comparisons_{tool.id}")