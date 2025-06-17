from django.urls import path
from . import views

app_name = 'ai_tools'

urlpatterns = [
    # Main listings
    path('', views.ToolListView.as_view(), name='tool_list'),
    path('explorer/', views.ToolExplorerView.as_view(), name='tool_explorer'),
    
    # Detail views
    path('tool/<slug:slug>/', views.ToolDetailView.as_view(), name='tool_detail'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('comparison/<int:pk>/', views.ToolComparisonView.as_view(), name='comparison_detail'),
    
    # Interactive features
    path('quiz/', views.ai_tool_quiz, name='tool_quiz'),
    path('quiz/results/', views.quiz_results, name='quiz_results'),
    
    # Submission
    path('submit-tool/', views.ToolSubmissionView.as_view(), name='submit_tool'),
    path('submission-thanks/', views.submission_thanks, name='submission_thanks'),
]