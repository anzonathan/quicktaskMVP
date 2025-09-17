from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.validators import RegexValidator

class RegistrationForm(UserCreationForm):
    # Validator for Ugandan phone numbers
    ugandan_phone_regex = RegexValidator(
        regex=r'^((\+256|0)7(0|1|5|6|7|8|9)[0-9]{7})$',
        message="Enter a valid Ugandan phone number, e.g., 0772123456 or +256772123456"
    )

    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'input'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'input'}))
    phone_number = forms.CharField(validators=[ugandan_phone_regex], max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'input'}))
    ROLE_CHOICES = Profile.ROLE_CHOICES
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select)
    district = forms.ChoiceField(choices=Profile.UGANDA_DISTRICTS, widget=forms.Select)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'district']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                role=self.cleaned_data.get('role'),
                district=self.cleaned_data.get('district'),
                phone_number=self.cleaned_data.get('phone_number')
            )
        return user