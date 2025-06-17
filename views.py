from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.core.cache import cache
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator
from .models import AITool, Category, ToolComparison, ToolSubmission, AdPlacement
from .forms import ToolSubmissionForm
from .utils import get_featured_tools, get_tool_recommendations

class ToolListView(ListView):
    model = AITool
    template_name = 'ai_tools/tool_list.html'
    context_object_name = 'tools'
    paginate_by = 24
    
    def get_queryset(self):
        cache_key = f"tool_list_{self.request.GET.urlencode()}"
        queryset = cache.get(cache_key)
        
        if not queryset:
            queryset = AITool.objects.filter(is_featured=True).order_by('-popularity_score')
            
            # Filtering
            category = self.request.GET.get('category')
            pricing = self.request.GET.get('pricing')
            search = self.request.GET.get('q')
            complexity = self.request.GET.get('complexity')
            
            if category:
                queryset = queryset.filter(categories__slug=category)
            if pricing:
                queryset = queryset.filter(pricing_type=pricing)
            if complexity:
                queryset = queryset.filter(technical_complexity__lte=complexity)
            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(short_description__icontains=search) |
                    Q(description__icontains=search)
                )
            
            # Annotate with usage count for sorting
            queryset = queryset.annotate(usage_count=Count('comparisons'))
            cache.set(cache_key, queryset, 60 * 15)  # Cache for 15 minutes
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(tool_count=Count('tools'))
        context['pricing_types'] = AITool.PRICING_TYPES
        context['featured_tools'] = get_featured_tools()[:6]
        context['ad_placements'] = AdPlacement.objects.filter(is_active=True)
        return context

class ToolDetailView(DetailView):
    model = AITool
    template_name = 'ai_tools/tool_detail.html'
    context_object_name = 'tool'
    slug_field = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tool = self.object
        
        # Increment view count
        tool.view_count += 1
        tool.save()
        
        # Get similar tools
        context['similar_tools'] = get_tool_recommendations(tool.id)[:5]
        
        # Get comparisons featuring this tool
        context['comparisons'] = ToolComparison.objects.filter(
            tools=tool
        ).order_by('-updated')[:3]
        
        # Get ads for detail page
        context['detail_ads'] = AdPlacement.objects.filter(
            placement_type__in=['DETAIL_SIDEBAR', 'INLINE'],
            is_active=True
        )
        
        return context

class ToolComparisonView(DetailView):
    model = ToolComparison
    template_name = 'ai_tools/comparison_detail.html'
    context_object_name = 'comparison'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_placements'] = AdPlacement.objects.filter(
            placement_type__in=['COMPARE_TOP'],
            is_active=True
        )
        
        # Increment view count
        comparison = self.object
        comparison.view_count += 1
        comparison.save()
        
        return context

class ToolExplorerView(TemplateView):
    template_name = 'ai_tools/tool_explorer.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tools = AITool.objects.only(
            'id', 'name', 'slug', 'pricing_type', 
            'technical_complexity', 'use_case_matrix'
        )
        
        context['tools_json'] = [{
            'id': tool.id,
            'name': tool.name,
            'slug': tool.slug,
            'pricing_type': tool.pricing_type,
            'technical_complexity': tool.technical_complexity,
            'use_case_matrix': tool.use_case_matrix or {},
            'primary_category': tool.primary_category.name if tool.primary_category else 'Other'
        } for tool in tools]
        
        context['categories'] = Category.objects.all()
        context['pricing_types'] = dict(AITool.PRICING_TYPES)
        return context

class CategoryDetailView(ListView):
    model = AITool
    template_name = 'ai_tools/category_detail.html'
    context_object_name = 'tools'
    paginate_by = 24
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return AITool.objects.filter(categories=self.category).order_by('-popularity_score')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['subcategories'] = self.category.children.all()
        context['popular_tools'] = self.get_queryset().order_by('-view_count')[:5]
        context['new_tools'] = self.get_queryset().order_by('-created')[:4]
        return context

def ai_tool_quiz(request):
    if request.method == 'POST':
        # Process quiz answers
        use_case = request.POST.get('use_case')
        budget = request.POST.get('budget')
        expertise = request.POST.get('expertise')
        
        # Get recommendations based on answers
        tools = AITool.objects.filter(
            Q(use_case_matrix__has_key=use_case) if use_case else Q(),
            pricing_type__lte=budget,
            technical_complexity__lte=expertise
        ).order_by('-popularity_score')[:5]
        
        return render(request, 'ai_tools/quiz_results.html', {
            'tools': tools,
            'criteria': {
                'use_case': use_case,
                'budget': budget,
                'expertise': expertise
            }
        })
    
    return render(request, 'ai_tools/quiz_start.html')

class ToolSubmissionView(CreateView):
    model = ToolSubmission
    form_class = ToolSubmissionForm
    template_name = 'ai_tools/tool_submission.html'
    success_url = reverse_lazy('ai_tools:submission_thanks')
    
    def form_valid(self, form):
        form.instance.submitted_by = self.request.user if self.request.user.is_authenticated else None
        response = super().form_valid(form)
        messages.success(self.request, 'Thank you for your submission! Our team will review it shortly.')
        return response

def submission_thanks(request):
    return render(request, 'ai_tools/submission_thanks.html')