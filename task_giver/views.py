from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Task
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal

@csrf_exempt
@login_required
def dashboard(request):
    return render(request, 'task_giver/dashboard.html')


def post_job(request):

    if request.method == 'POST':
        # Get the form data from the POST request
        title = request.POST.get('task-title')
        description = request.POST.get('task-description')
        budget_str = request.POST.get('budget')
        deadline_str = request.POST.get('deadline')
        file_upload = request.FILES.get('file-upload')

        # Basic validation
        if not all([title, description, budget_str]):
            messages.error(request, 'Please fill out all required fields.')
            return render(request, 'task_giver/postjob.html')

        try:
            # Convert budget to a Decimal for financial accuracy
            budget = Decimal(budget_str)
        except (ValueError, TypeError):
            messages.error(request, 'Please enter a valid budget.')
            return render(request, 'task_giver/postjob.html')

        # Convert deadline to a datetime object if it exists
        deadline = None
        if deadline_str:
            try:
                deadline = timezone.datetime.strptime(deadline_str, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, 'Please enter a valid date.')
                return render(request, 'task_giver/postjob.html')

        # Create and save the new Task object
        new_task = Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            budget=budget,
            deadline=deadline,
            file_upload=file_upload
        )
        
        # Display a success message and redirect
        messages.success(request, 'Your task has been posted successfully!')
        return redirect('dashboard.tg')  # Redirect to the dashboard or a success page

    # If the request is a GET, render the form page
    return render(request, 'task_giver/postjob.html')

@login_required(login_url='users/login')
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

    # Render the task_detail.html template, passing the task object to the context.
    return render(request, 'task_giver/task_detail.html', {'task': task})