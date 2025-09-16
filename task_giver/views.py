from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Task, Applications
from accounts.models import Profile
from django.contrib import messages
from .forms import TaskForm
from django.utils import timezone
from decimal import Decimal

@login_required
def dashboard(request):
    first_name = request.user.first_name
    location = request.user.profile.district
    return render(request, 'task_giver/dashboard.html', {'first_name': first_name, 'location': location})

####################
##### JOB Posts ####
#####################

@login_required
def postjob(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task posted successfully!')
            return redirect('task_giver:postings')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = TaskForm()
    return render(request, 'task_giver/postjob.html', {'form': form})

@login_required
def postings(request):
    # Filter the tasks to only include those posted by the current user.
    user_tasks = Task.objects.filter(user=request.user).order_by('-posted_on')
    
    context = {
        'tasks': user_tasks
    }
    
    return render(request, 'task_giver/postings.html', context)

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'task_giver/task_detail.html', {'task': task})

@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_giver:task_detail', task_id=task.id)
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_giver/postjob.html', {'form': form})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_giver:postings')
    return redirect('task_giver:postings')

###########################
##### JOB Applications ####
###########################

@login_required
def applications(request):
    apps = Applications.objects.filter(task__user=request.user)

    context = {
        'apps': apps
    }
    return render(request, 'task_giver/applications.html',context)