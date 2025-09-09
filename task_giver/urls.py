from django.urls import path
from . import views

app_name = 'task_giver'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('postjob/', views.postjob, name='postjob'),
    path('postings/', views.postings, name='postings'),
    path('postings/<int:task_id>/', views.task_detail, name='task_detail'),
    path('postings/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('postings/<int:task_id>/delete/', views.task_delete, name='task_delete'),
]
