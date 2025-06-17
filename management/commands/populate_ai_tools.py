from django.core.management.base import BaseCommand
from ai_tools.models import AITool, Category
import json

class Command(BaseCommand):
    help = 'Populate the database with sample AI tools'
    
    def handle(self, *args, **options):
        # Create categories first
        categories_data = [
            {'name': 'Text & Content', 'slug': 'text-content', 'icon': 'fas fa-pen-fancy'},
            {'name': 'Image & Design', 'slug': 'image-design', 'icon': 'fas fa-image'},
            {'name': 'Video & Animation', 'slug': 'video-animation', 'icon': 'fas fa-video'},
            {'name': 'Audio & Speech', 'slug': 'audio-speech', 'icon': 'fas fa-microphone'},
            {'name': 'Code & Development', 'slug': 'code-development', 'icon': 'fas fa-code'},
            {'name': 'Agents & Automation', 'slug': 'agents-automation', 'icon': 'fas fa-robot'},
            {'name': 'Productivity & Business', 'slug': 'productivity-business', 'icon': 'fas fa-briefcase'},
            {'name': 'Education & Research', 'slug': 'education-research', 'icon': 'fas fa-graduation-cap'},
            {'name': 'Data Analysis', 'slug': 'data-analysis', 'icon': 'fas fa-chart-line'},
            {'name': 'Marketing & Sales', 'slug': 'marketing-sales', 'icon': 'fas fa-bullhorn'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f"Created category: {category.name}")
        
        # Sample AI tools data
        tools_data = [
            {
                'name': 'ChatGPT',
                'website': 'https://chat.openai.com',
                'short_description': 'Advanced conversational AI for text generation, coding, and problem-solving.',
                'description': 'ChatGPT is a state-of-the-art language model developed by OpenAI that can engage in human-like conversations, generate creative content, write code, solve complex problems, and assist with a wide variety of tasks. It uses advanced transformer architecture to understand context and provide relevant, helpful responses.',
                'pricing_type': 'FRP',
                'price_range': '$0-$20/month',
                'api_available': True,
                'open_source': False,
                'deployment_options': 'Cloud',
                'technical_complexity': 2,
                'use_case_matrix': {
                    'content_creation': 9,
                    'coding': 8,
                    'research': 8,
                    'education': 9
                },
                'is_featured': True,
                'popularity_score': 9.5,
                'categories': ['text-content', 'code-development']
            },
            {
                'name': 'Midjourney',
                'website': 'https://midjourney.com',
                'short_description': 'AI-powered image generation tool for creating stunning artwork and designs.',
                'description': 'Midjourney is an independent research lab that produces an AI program that creates images from textual descriptions. It\'s known for its artistic and creative output, making it popular among artists, designers, and content creators.',
                'pricing_type': 'SUB',
                'price_range': '$10-$60/month',
                'api_available': False,
                'open_source': False,
                'deployment_options': 'Cloud',
                'technical_complexity': 3,
                'use_case_matrix': {
                    'content_creation': 10,
                    'design': 10,
                    'marketing': 8
                },
                'is_featured': True,
                'popularity_score': 9.2,
                'categories': ['image-design']
            },
            {
                'name': 'GitHub Copilot',
                'website': 'https://github.com/features/copilot',
                'short_description': 'AI pair programmer that helps you write code faster and with fewer errors.',
                'description': 'GitHub Copilot is an AI coding assistant that provides autocomplete-style suggestions as you code. It\'s trained on billions of lines of code and can help with various programming languages and frameworks.',
                'pricing_type': 'SUB',
                'price_range': '$10-$19/month',
                'api_available': True,
                'open_source': False,
                'deployment_options': 'Cloud,IDE',
                'technical_complexity': 4,
                'use_case_matrix': {
                    'coding': 10,
                    'productivity': 9,
                    'education': 7
                },
                'is_featured': True,
                'popularity_score': 8.8,
                'categories': ['code-development']
            },
            {
                'name': 'Stable Diffusion',
                'website': 'https://stability.ai',
                'short_description': 'Open-source text-to-image AI model for generating high-quality images.',
                'description': 'Stable Diffusion is a deep learning, text-to-image model that can generate detailed images conditioned on text descriptions. It\'s open-source and can be run locally or in the cloud.',
                'pricing_type': 'FRE',
                'price_range': 'Free',
                'api_available': True,
                'open_source': True,
                'deployment_options': 'Cloud,On-Prem,Local',
                'technical_complexity': 6,
                'use_case_matrix': {
                    'content_creation': 9,
                    'design': 9,
                    'research': 7
                },
                'is_featured': True,
                'popularity_score': 8.5,
                'categories': ['image-design']
            },
            {
                'name': 'Notion AI',
                'website': 'https://notion.so/ai',
                'short_description': 'AI writing assistant integrated into Notion for enhanced productivity.',
                'description': 'Notion AI is built into Notion to help you write, brainstorm, edit, summarize and more. It can help with various writing tasks and boost productivity within the Notion workspace.',
                'pricing_type': 'SUB',
                'price_range': '$8-$15/month',
                'api_available': False,
                'open_source': False,
                'deployment_options': 'Cloud',
                'technical_complexity': 2,
                'use_case_matrix': {
                    'content_creation': 8,
                    'productivity': 9,
                    'organization': 8
                },
                'is_featured': False,
                'popularity_score': 7.8,
                'categories': ['productivity-business', 'text-content']
            },
            {
                'name': 'RunwayML',
                'website': 'https://runwayml.com',
                'short_description': 'AI-powered video editing and generation platform for creators.',
                'description': 'RunwayML offers a suite of AI tools for video editing, including background removal, object tracking, and AI-generated video content. It\'s designed for content creators and filmmakers.',
                'pricing_type': 'FRP',
                'price_range': '$0-$35/month',
                'api_available': True,
                'open_source': False,
                'deployment_options': 'Cloud',
                'technical_complexity': 4,
                'use_case_matrix': {
                    'content_creation': 9,
                    'video_editing': 10,
                    'design': 8
                },
                'is_featured': False,
                'popularity_score': 8.0,
                'categories': ['video-animation']
            },
            {
                'name': 'Whisper',
                'website': 'https://openai.com/research/whisper',
                'short_description': 'Automatic speech recognition system by OpenAI.',
                'description': 'Whisper is an automatic speech recognition (ASR) system trained on 680,000 hours of multilingual and multitask supervised data collected from the web.',
                'pricing_type': 'FRE',
                'price_range': 'Free',
                'api_available': True,
                'open_source': True,
                'deployment_options': 'Cloud,On-Prem,Local',
                'technical_complexity': 5,
                'use_case_matrix': {
                    'transcription': 10,
                    'accessibility': 9,
                    'content_creation': 7
                },
                'is_featured': False,
                'popularity_score': 8.3,
                'categories': ['audio-speech']
            },
            {
                'name': 'LangChain',
                'website': 'https://langchain.com',
                'short_description': 'Framework for developing applications powered by language models.',
                'description': 'LangChain is a framework for developing applications powered by language models. It enables applications that are context-aware and can reason about their environment.',
                'pricing_type': 'FRE',
                'price_range': 'Free',
                'api_available': True,
                'open_source': True,
                'deployment_options': 'Cloud,On-Prem,Local',
                'technical_complexity': 8,
                'use_case_matrix': {
                    'development': 10,
                    'automation': 9,
                    'integration': 9
                },
                'is_featured': False,
                'popularity_score': 8.7,
                'categories': ['agents-automation', 'code-development']
            },
            {
                'name': 'Jasper',
                'website': 'https://jasper.ai',
                'short_description': 'AI content platform for enterprise marketing teams.',
                'description': 'Jasper is an AI content platform that helps teams create high-quality content faster. It\'s designed for marketing teams and offers brand voice customization.',
                'pricing_type': 'SUB',
                'price_range': '$39-$125/month',
                'api_available': True,
                'open_source': False,
                'deployment_options': 'Cloud',
                'technical_complexity': 3,
                'use_case_matrix': {
                    'content_creation': 9,
                    'marketing': 10,
                    'copywriting': 9
                },
                'is_featured': False,
                'popularity_score': 8.1,
                'categories': ['marketing-sales', 'text-content']
            },
            {
                'name': 'Perplexity AI',
                'website': 'https://perplexity.ai',
                'short_description': 'AI-powered search engine that provides accurate answers with sources.',
                'description': 'Perplexity AI is an AI-powered search engine that provides accurate, real-time answers to questions with cited sources. It combines the power of large language models with up-to-date information.',
                'pricing_type': 'FRP',
                'price_range': '$0-$20/month',
                'api_available': True,
                'open_source': False,
                'deployment_options': 'Cloud',
                'technical_complexity': 2,
                'use_case_matrix': {
                    'research': 10,
                    'education': 9,
                    'fact_checking': 10
                },
                'is_featured': False,
                'popularity_score': 8.4,
                'categories': ['education-research']
            }
        ]
        
        # Create tools
        for tool_data in tools_data:
            categories = tool_data.pop('categories', [])
            tool, created = AITool.objects.get_or_create(
                name=tool_data['name'],
                defaults=tool_data
            )
            
            if created:
                # Add categories
                for cat_slug in categories:
                    try:
                        category = Category.objects.get(slug=cat_slug)
                        tool.categories.add(category)
                    except Category.DoesNotExist:
                        pass
                
                self.stdout.write(f"Created tool: {tool.name}")
            else:
                self.stdout.write(f"Tool already exists: {tool.name}")
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated AI tools database!')
        )