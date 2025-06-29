# Generated by Django 5.1.4 on 2025-06-17 05:50

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdPlacement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('placement_type', models.CharField(choices=[('HERO', 'Hero Banner'), ('SIDEBAR', 'Sidebar'), ('COMPARE_TOP', 'Comparison Top'), ('INLINE', 'Inline Content'), ('DETAIL_SIDEBAR', 'Detail Sidebar')], max_length=20, unique=True)),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('code_snippet', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=120, unique=True)),
                ('icon', models.CharField(blank=True, help_text='FontAwesome icon class', max_length=50)),
                ('description', models.TextField(blank=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='ai_tools.category')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='AITool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=220, unique=True)),
                ('website', models.URLField()),
                ('logo', models.ImageField(blank=True, null=True, upload_to='ai_tools/logos/')),
                ('short_description', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('pricing_type', models.CharField(choices=[('FRE', 'Free'), ('FRP', 'Freemium'), ('SUB', 'Subscription'), ('PAY', 'Pay-per-use'), ('COM', 'Commercial')], max_length=3)),
                ('price_range', models.CharField(blank=True, max_length=100)),
                ('api_available', models.BooleanField(default=False)),
                ('open_source', models.BooleanField(default=False)),
                ('deployment_options', models.TextField(blank=True, help_text="Comma-separated options like 'Cloud,On-Prem,Hybrid'")),
                ('technical_complexity', models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('use_case_matrix', models.JSONField(blank=True, help_text='{"content_creation": 8, "data_analysis": 9}', null=True)),
                ('affiliate_link', models.URLField(blank=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('last_verified', models.DateField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('popularity_score', models.FloatField(default=0.0)),
                ('categories', models.ManyToManyField(related_name='tools', to='ai_tools.category')),
                ('features', models.ManyToManyField(blank=True, related_name='tools', to='ai_tools.feature')),
            ],
            options={
                'ordering': ['-is_featured', '-popularity_score', '-last_verified'],
            },
        ),
        migrations.CreateModel(
            name='ToolComparison',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=220, unique=True)),
                ('comparison_data', models.JSONField(help_text='Structured comparison data')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('tools', models.ManyToManyField(related_name='comparisons', to='ai_tools.aitool')),
            ],
        ),
        migrations.CreateModel(
            name='ToolSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('website', models.URLField()),
                ('description', models.TextField()),
                ('pricing_type', models.CharField(choices=[('FRE', 'Free'), ('FRP', 'Freemium'), ('SUB', 'Subscription'), ('PAY', 'Pay-per-use'), ('COM', 'Commercial')], max_length=3)),
                ('submitter_name', models.CharField(max_length=100)),
                ('submitter_email', models.EmailField(max_length=254)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending Review'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10)),
                ('notes', models.TextField(blank=True)),
                ('categories', models.ManyToManyField(to='ai_tools.category')),
            ],
        ),
        migrations.AddIndex(
            model_name='aitool',
            index=models.Index(fields=['slug'], name='ai_tools_ai_slug_ebd90d_idx'),
        ),
        migrations.AddIndex(
            model_name='aitool',
            index=models.Index(fields=['pricing_type'], name='ai_tools_ai_pricing_810051_idx'),
        ),
        migrations.AddIndex(
            model_name='aitool',
            index=models.Index(fields=['is_featured'], name='ai_tools_ai_is_feat_be9a4c_idx'),
        ),
    ]
