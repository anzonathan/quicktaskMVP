from django.db import models
from django.conf import settings
from task_giver.models import Task # Assuming Task model is in the same app

class SavedTask(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_tasks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        # Ensures that a user can only save a specific task once.
        unique_together = ('user', 'task')
        verbose_name = 'Saved Task'
        verbose_name_plural = 'Saved Tasks'

    def __str__(self):
        return f"{self.user.username} saved {self.task.title}"



