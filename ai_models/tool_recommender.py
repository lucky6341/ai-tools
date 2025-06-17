import joblib
import numpy as np
from sklearn.neighbors import NearestNeighbors
from django.conf import settings
import os
from ..models import AITool

class ToolRecommender:
    def __init__(self):
        self.model_path = os.path.join(settings.BASE_DIR, 'ai_tools', 'ai_models', 'tool_recommender.pkl')
        self.model = self.load_model()
    
    def load_model(self):
        try:
            return joblib.load(self.model_path)
        except:
            return None
    
    def train_model(self):
        tools = AITool.objects.all()
        if tools.count() < 10:  # Minimum tools to train
            return False
        
        # Create feature matrix
        features = []
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
        
        X = np.array(features)
        
        # Normalize features
        X = (X - X.mean(axis=0)) / X.std(axis=0)
        
        # Train model
        self.model = NearestNeighbors(n_neighbors=6, metric='cosine')
        self.model.fit(X)
        
        # Save model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
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
            
            # Normalize
            target = (target - self.model._fit_X.mean(axis=0)) / self.model._fit_X.std(axis=0)
            
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