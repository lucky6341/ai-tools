from django.core.cache import cache
from django.db.models import Count
from .models import AITool, Category
import joblib
import numpy as np
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
    """Get similar tools using ML recommendations"""
    cache_key = f"tool_recs_{tool_id}"
    recommendations = cache.get(cache_key)
    
    if not recommendations:
        try:
            recommender = ToolRecommender()
            similar_ids = recommender.recommend(tool_id, n)
            recommendations = list(AITool.objects.filter(id__in=similar_ids))
            cache.set(cache_key, recommendations, 60 * 60 * 24)  # Cache for 24 hours
        except Exception as e:
            # Fallback to popularity-based recommendations
            recommendations = list(AITool.objects.annotate(num_comps=Count('comparisons'))
                                 .order_by('-num_comps')[:n])
    return recommendations

def get_trending_tools(days=30, limit=5):
    """Get recently popular tools"""
    since = datetime.now() - timedelta(days=days)
    return list(AITool.objects.filter(comparisons__created__gte=since)
               .annotate(num_comps=Count('comparisons'))
               .order_by('-num_comps')[:limit])

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

class ToolRecommender:
    def __init__(self):
        self.model_path = 'ai_tools/ai_models/tool_recommender.pkl'
        self.model = self.load_model()
        self.feature_names = ['content', 'data', 'coding', 'research', 'price', 'complexity']
    
    def load_model(self):
        try:
            return joblib.load(self.model_path)
        except:
            return None
    
    def train_model(self):
        tools = AITool.objects.all()
        if not tools:
            return False
        
        # Create feature matrix
        features = []
        tool_ids = []
        for tool in tools:
            # Feature vector: [content_creation, data_analysis, coding, research, price, complexity]
            features.append([
                tool.use_case_matrix.get('content_creation', 0),
                tool.use_case_matrix.get('data_analysis', 0),
                tool.use_case_matrix.get('coding', 0),
                tool.use_case_matrix.get('research', 0),
                self._get_price_value(tool.price_range),
                tool.technical_complexity
            ])
            tool_ids.append(tool.id)
        
        X = np.array(features)
        
        # Train model
        self.model = NearestNeighbors(n_neighbors=6, metric='cosine')
        self.model.fit(X)
        
        # Save model
        joblib.dump(self.model, self.model_path)
        return True
    
    def recommend(self, tool_id, n=5):
        if not self.model:
            return []
        
        try:
            tool = AITool.objects.get(id=tool_id)
            all_tools = list(AITool.objects.all())
            
            # Create target vector
            target = np.array([
                tool.use_case_matrix.get('content_creation', 0),
                tool.use_case_matrix.get('data_analysis', 0),
                tool.use_case_matrix.get('coding', 0),
                tool.use_case_matrix.get('research', 0),
                self._get_price_value(tool.price_range),
                tool.technical_complexity
            ]).reshape(1, -1)
            
            # Find nearest neighbors
            distances, indices = self.model.kneighbors(target, n_neighbors=n+1)
            
            # Return tool IDs (excluding the target itself)
            return [all_tools[i].id for i in indices[0][1:n+1]]
        except:
            return []
    
    def _get_price_value(self, price_range):
        """Convert price range to numeric value"""
        if not price_range:
            return 0
        try:
            if price_range.lower() == 'free':
                return 0
            elif '-' in price_range:
                low, high = price_range.split('-')
                return (float(low.strip().replace('$', '')) + float(high.strip().replace('$', ''))) / 2
            else:
                return float(price_range.replace('$', '').strip())
        except:
            return 0

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
                tool.use_case_matrix.get('max_input_length', 'N/A'),
                tool.use_case_matrix.get('output_quality', 'N/A'),
                ', '.join(tool.use_case_matrix.get('languages', [])[:3]) or 'N/A',
                'Yes' if tool.api_available else 'No',
                'Yes' if tool.pricing_type in ['FRE', 'FRP'] else 'No'
            ]
        }
    
    return comparison_data