from django.urls import path
from . import views

app_name = 'task_seeker'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('job_posts/',views.job_posts, name="job_posts"),
    path('job_posts/<int:task_id>/save_task', views.save_task, name='save_task'),

] 