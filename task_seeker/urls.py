from django.urls import path
from . import views

app_name = 'task_seeker'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my_jobs/',views.my_jobs, name="my_jobs"),
    path('job_posts/',views.job_posts, name="job_posts"),
    path('job_posts/<int:task_id>/save_task', views.save_task, name='save_task'),
    path('job_posts/<int:task_id>/apply', views.apply, name='apply'),
    #Applications
    path('applications/', views.seeker_apps, name="seeker_apps" ),
    path('applications/<int:app_id>/withdraw', views.withdraw_app, name="withdraw_app" ),
    path('applications/<int:task_id>/accept', views.accept_app, name="accept_app" ),
    path('applications//<int:app_id>/decline', views.decline_app, name="decline_app" ),



] 