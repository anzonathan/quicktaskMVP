from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = [
        ('seeker', 'Task Seeker'),
        ('giver', 'Task Giver'),
    ]

    UGANDA_DISTRICTS = [
        ('Kampala', 'Kampala'),
        ('Wakiso', 'Wakiso'),
        ('Mukono', 'Mukono'),
        ('Mbarara', 'Mbarara'),
        ('Gulu', 'Gulu'),
        ('Jinja', 'Jinja'),
        ('Mbale', 'Mbale'),
        ('Arua', 'Arua'),
        ('Lira', 'Lira'),
        ('Masaka', 'Masaka'),
        ('Fort Portal', 'Fort Portal'),
        ('Hoima', 'Hoima'),
        ('Soroti', 'Soroti'),
        ('Masindi', 'Masindi'),
        ('Kabale', 'Kabale'),
        ('Bushenyi', 'Bushenyi'),
        ('Tororo', 'Tororo'),
        ('Iganga', 'Iganga'),
        ('Mityana', 'Mityana'),
        ('Kasese', 'Kasese'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    district = models.CharField(max_length=50, choices=UGANDA_DISTRICTS, default='Kampala')

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
