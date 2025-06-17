from .models import Category, AITool
from django.core.cache import cache
from django.db.models import Count

def ai_tools_context(request):
    """Add AI tools context to all templates"""
    
    def get_categories():
        cache_key = "all_categories"
        categories = cache.get(cache_key)
        if not categories:
            categories = Category.objects.annotate(tool_count=Count('tools')).filter(tool_count__gt=0)
            cache.set(cache_key, categories, 60 * 60 * 12)  # Cache for 12 hours
        return categories

    def get_featured_tools():
        cache_key = "featured_tools_header"
        tools = cache.get(cache_key)
        if not tools:
            tools = AITool.objects.filter(is_featured=True).order_by('-popularity_score')[:3]
            cache.set(cache_key, tools, 60 * 60 * 6)  # Cache for 6 hours
        return tools

    return {
        'ai_categories': get_categories(),
        'featured_ai_tools': get_featured_tools(),
        'ai_tools_base': 'ai_tools/'  # Base template path
    }