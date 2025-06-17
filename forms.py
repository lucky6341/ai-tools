from django import forms
from .models import ToolSubmission

class ToolSubmissionForm(forms.ModelForm):
    class Meta:
        model = ToolSubmission
        fields = ['name', 'website', 'description', 'categories', 'pricing_type', 
                  'submitter_name', 'submitter_email']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'categories': forms.CheckboxSelectMultiple,
        }
    
    def clean_website(self):
        website = self.cleaned_data['website']
        if not website.startswith('http'):
            website = 'https://' + website
        return website