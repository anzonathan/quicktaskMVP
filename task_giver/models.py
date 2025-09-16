from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db.models import UniqueConstraint

# This model represents a task that a user can post.
class Task(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateTimeField()
    
    posted_on = models.DateTimeField(auto_now_add=True)

    views = models.PositiveIntegerField(default=0)

    
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    file_upload = models.FileField(upload_to='task_files/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    
    # New location field
    location = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title

class Applications(models.Model):
        applied_on = models.DateTimeField(auto_now_add=True)
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        task = models.ForeignKey(Task, on_delete=models.CASCADE)
            
        STATUS_CHOICES = (
            ('review', 'Review'),
            ('rejected', 'Rejected'),
            ('approved', 'Approved'),
        )
        status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

        class Meta:
            constraints = [
                 UniqueConstraint(fields=['user','task'], name="applications_must_be_unqiue")
            ]
