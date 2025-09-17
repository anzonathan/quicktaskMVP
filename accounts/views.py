from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from .models import Profile


def register(request):
    """
    Handles user registration with a custom form.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            
            # Retrieve data for the profile
            role = form.cleaned_data['role']
            district = form.cleaned_data.get('district')
            phone_number = form.cleaned_data.get('phone_number')
            
            # Create or get the profile and save the new data
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = role
            profile.phone_number = phone_number # Add this line
            if district:
                profile.district = district
            profile.save()
            
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('accounts:login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm(request)
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('home.index')

@csrf_exempt
@login_required
def dashboard(request):
    profile = Profile.objects.filter(user=request.user).first()
    role = profile.role if profile else 'seeker'
    if role == 'giver':
        return redirect('task_giver:dashboard')
    return redirect('task_seeker:dashboard')