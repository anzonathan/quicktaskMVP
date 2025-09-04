from django.urls import path
from . import views

app_name = 'task_giver'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/postjob/',views.post_job, name="postjob"),
    path('dashboard/postings/',views.postings, name="postings"),
    path('my_postings/<int:task_id>/', views.task_detail, name='task_detail')
] 


