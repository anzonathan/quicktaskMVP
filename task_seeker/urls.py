from django.urls import path
from . import views

app_name = 'task_seeker'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
] 