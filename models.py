from django.db import models
from django.db.models import JSONField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def tool_count(self):
        return self.tools.count()


class Feature(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AITool(models.Model):
    PRICING_TYPES = [
        ('FRE', 'Free'),
        ('FRP', 'Freemium'),
        ('SUB', 'Subscription'),
        ('PAY', 'Pay-per-use'),
        ('COM', 'Commercial'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    website = models.URLField()
    logo = models.ImageField(upload_to='ai_tools/logos/', blank=True, null=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='tools')
    features = models.ManyToManyField(Feature, related_name='tools', blank=True)
    pricing_type = models.CharField(max_length=3, choices=PRICING_TYPES)
    price_range = models.CharField(max_length=100, blank=True)
    api_available = models.BooleanField(default=False)
    open_source = models.BooleanField(default=False)

    deployment_options = models.TextField(
        blank=True,
        help_text="Comma-separated options like 'Cloud,On-Prem,Hybrid'"
    )

    technical_complexity = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    use_case_matrix = JSONField(
        blank=True, 
        null=True,
        help_text='{"content_creation": 8, "data_analysis": 9}'
    )
    affiliate_link = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    last_verified = models.DateField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)
    popularity_score = models.FloatField(default=0.0)

    class Meta:
        ordering = ['-is_featured', '-popularity_score', '-last_verified']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['pricing_type']),
            models.Index(fields=['is_featured']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ai_tools:tool_detail', kwargs={'slug': self.slug})

    @property
    def primary_category(self):
        return self.categories.first()

    @property
    def like_count(self):
        # Placeholder for future implementation
        return 0

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while AITool.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ToolComparison(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    tools = models.ManyToManyField(AITool, related_name='comparisons')
    comparison_data = JSONField(
        help_text='Structured comparison data'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ai_tools:comparison_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while ToolComparison.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ToolSubmission(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    name = models.CharField(max_length=200)
    website = models.URLField()
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    pricing_type = models.CharField(max_length=3, choices=AITool.PRICING_TYPES)
    submitter_name = models.CharField(max_length=100)
    submitter_email = models.EmailField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"


class AdPlacement(models.Model):
    PLACEMENT_CHOICES = [
        ('HERO', 'Hero Banner'),
        ('SIDEBAR', 'Sidebar'),
        ('COMPARE_TOP', 'Comparison Top'),
        ('INLINE', 'Inline Content'),
        ('DETAIL_SIDEBAR', 'Detail Sidebar'),
    ]

    name = models.CharField(max_length=100)
    placement_type = models.CharField(max_length=20, choices=PLACEMENT_CHOICES, unique=True)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    code_snippet = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (${self.base_price}/mo)"