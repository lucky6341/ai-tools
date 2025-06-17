from django.core.cache import cache
from django.db.models import Count
from .models import AITool, Category
import json
from datetime import datetime, timedelta

def get_featured_tools(limit=6):
    cache_key = "featured_tools"
    tools = cache.get(cache_key)
    if not tools:
        tools = list(AITool.objects.filter(is_featured=True)
                      .order_by('-popularity_score')[:limit])
        cache.set(cache_key, tools, 60 * 60 * 6)  # Cache for 6 hours
    return tools

def get_tool_recommendations(tool_id, n=5):
    """Get similar tools using basic similarity"""
    cache_key = f"tool_recs_{tool_id}"
    recommendations = cache.get(cache_key)
    
    if not recommendations:
        try:
            tool = AITool.objects.get(id=tool_id)
            # Get tools from same categories
            similar_tools = AITool.objects.filter(
                categories__in=tool.categories.all()
            ).exclude(id=tool_id).distinct()
            
            # If not enough, get popular tools
            if similar_tools.count() < n:
                popular_tools = AITool.objects.exclude(id=tool_id).order_by('-popularity_score')
                recommendations = list(similar_tools[:n//2]) + list(popular_tools[:n//2])
            else:
                recommendations = list(similar_tools.order_by('-popularity_score')[:n])
            
            cache.set(cache_key, recommendations, 60 * 60 * 24)  # Cache for 24 hours
        except AITool.DoesNotExist:
            recommendations = list(AITool.objects.order_by('-popularity_score')[:n])
    
    return recommendations

def get_trending_tools(days=30, limit=5):
    """Get recently popular tools"""
    since = datetime.now() - timedelta(days=days)
    return list(AITool.objects.filter(created__gte=since)
               .order_by('-view_count', '-popularity_score')[:limit])

def get_category_tree():
    """Get hierarchical category structure"""
    cache_key = "category_tree"
    tree = cache.get(cache_key)
    if not tree:
        categories = Category.objects.all()
        tree = {}
        for cat in categories:
            if cat.parent_id:
                if cat.parent_id not in tree:
                    tree[cat.parent_id] = {'id': cat.parent_id, 'children': []}
                tree[cat.parent_id]['children'].append({
                    'id': cat.id,
                    'name': cat.name,
                    'slug': cat.slug,
                    'icon': cat.icon
                })
        cache.set(cache_key, tree, 60 * 60 * 24)  # Cache for 24 hours
    return tree

def generate_comparison_matrix(tools):
    """Generate comparison data for multiple tools"""
    comparison_data = {
        'features': ['Max Input Length', 'Output Quality', 'Languages Supported', 'API Access', 'Free Tier'],
        'tools': {}
    }
    
    for tool in tools:
        comparison_data['tools'][tool.id] = {
            'name': tool.name,
            'values': [
                tool.use_case_matrix.get('max_input_length', 'N/A') if tool.use_case_matrix else 'N/A',
                tool.use_case_matrix.get('output_quality', 'N/A') if tool.use_case_matrix else 'N/A',
                ', '.join(tool.use_case_matrix.get('languages', [])[:3]) if tool.use_case_matrix and tool.use_case_matrix.get('languages') else 'N/A',
                'Yes' if tool.api_available else 'No',
                'Yes' if tool.pricing_type in ['FRE', 'FRP'] else 'No'
            ]
        }
    
    return comparison_data