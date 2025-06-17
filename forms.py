from django import forms
from .models import ToolSubmission, Category

class ToolSubmissionForm(forms.ModelForm):
    class Meta:
        model = ToolSubmission
        fields = ['name', 'website', 'description', 'categories', 'pricing_type', 
                  'submitter_name', 'submitter_email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter the tool name'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://example.com'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'Describe what this tool does and its key features'
            }),
            'categories': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-checkbox'
            }),
            'pricing_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'submitter_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your name'
            }),
            'submitter_email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'your.email@example.com'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.all()
        self.fields['categories'].widget.attrs.update({'class': 'category-checkbox'})
    
    def clean_website(self):
        website = self.cleaned_data['website']
        if not website.startswith(('http://', 'https://')):
            website = 'https://' + website
        return website