from django import forms
from .models import Task
from accounts.models import Profile

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'budget', 'deadline', 'location', 'file_upload']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'e.g. Design a logo for a startup'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Provide a detailed description...', 'rows': '6'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'}),
            'budget': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'e.g. UGX 50,000 (Fixed price)'}),
            'deadline': forms.DateInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500', 'type': 'date'}),
            'location': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'}),
            'file_upload': forms.ClearableFileInput(attrs={'class': 'hidden'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customizing the location choices
        self.fields['location'].choices = Profile.UGANDA_DISTRICTS
