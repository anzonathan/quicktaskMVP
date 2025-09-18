from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.db import IntegrityError
import json

from task_giver.models import Task, Applications
from .models import SavedTask

@login_required
def dashboard(request):

    name = f'{request.user.first_name} {request.user.last_name}'

    context = {
        'name': name
    }

    return render(request, 'task_seeker/dashboard.html', context)

@login_required
def my_jobs(request):

    apps = Applications.objects.filter(user=request.user, task__status='In Progress')

    context = {
        'apps': apps
    }
    return render(request, 'task_seeker/jobs.html', context)


@login_required
def job_posts(request):
    # Fetch only jobs from the database that have a status of 'open'.
    jobs = list(Task.objects.filter(status='open').order_by('-posted_on').values(
        'id', 'title', 'user__username', 'posted_on', 'budget', 'deadline', 'location', 
        'category', 'description'
    ))
    
    # Get the IDs of all tasks saved by the current user.
    saved_job_ids = list(SavedTask.objects.filter(user=request.user).values_list('task_id', flat=True))

    # Convert date and decimal fields to a string format that can be serialized to JSON.
    for job in jobs:
        if job['posted_on']:
            job['posted_on'] = job['posted_on'].strftime('%Y-%m-%d')
        if job['deadline']:
            job['deadline'] = job['deadline'].strftime('%Y-%m-%d')
        # Convert Decimal budget to a string to make it JSON serializable
        if 'budget' in job:
            job['budget'] = str(job['budget'])

    context = {
        'jobs_json': json.dumps(jobs),
        'saved_jobs_json': json.dumps(saved_job_ids),
    }
    return render(request, "task_seeker/job_posts.html", context)

def save_task(request, task_id):
    """
    Toggles the saved status of a task for the current user and returns a JSON response.
    """
    if request.method == 'POST':
        user = request.user
        
        # Check for authentication.
        if not user.is_authenticated:
            # Return a JSON response for an unauthenticated user.
            return JsonResponse({'status': 'error', 'message': 'Authentication required.'}, status=401)

        # Use get_object_or_404 for a more Django-friendly way to handle a missing task.
        task = get_object_or_404(Task, pk=task_id)

        try:
            # Check if the task is already saved by the user
            saved_task = SavedTask.objects.get(user=user, task=task)
            saved_task.delete()
            # Return a success JSON response indicating the task was unsaved.
            return JsonResponse({'status': 'unsaved', 'message': 'Task unsaved.'})
        except SavedTask.DoesNotExist:
            # Task is not saved, so save it.
            SavedTask.objects.create(user=user, task=task)
            # Return a success JSON response indicating the task was saved.
            return JsonResponse({'status': 'saved', 'message': 'Task saved.'})
    
    # If the request method is not POST, return a 405 Method Not Allowed error.
    return JsonResponse({'status': 'error', 'message': 'Method not allowed.'}, status=405)

@login_required
def seeker_apps(request):

    apps = Applications.objects.filter(user=request.user, task__status='open')

    context = {
        'apps': apps
    }
    return render(request, 'task_seeker/applications.html', context)

@login_required
def apply(request, task_id):
    user = request.user
    new_application = Applications(user=user,task_id=task_id)
    new_application.save()
    return redirect('task_seeker:seeker_apps')

@login_required
def withdraw_app(request, app_id):

    app = get_object_or_404(Applications, pk=app_id, user=request.user)
    app.delete()

    messages.success(request,"Application Delete Successfully")

    return redirect('task_seeker:seeker_apps')

@login_required
def accept_app(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.status = "In Progress"
    task.save()

    messages.success(request,"Task is now in progress")

    return redirect('task_seeker:seeker_apps')

@login_required
def decline_app(request, app_id):
    app = get_object_or_404(Applications, pk=app_id, user=request.user)
    app.delete()

    messages.success(request,"Application Delete Successfully")

    return redirect('task_seeker:seeker_apps')