from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

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

    ugandan_phone_regex = RegexValidator(
        regex=r'^((\+256|0)7(0|1|5|6|7|8|9)[0-9]{7})$',
        message="Enter a valid Ugandan phone number, e.g., 0772123456 or +256772123456"
    )

    phone_number = models.CharField(
        validators=[ugandan_phone_regex],
        max_length=15, # Set an appropriate max length
        blank=True, # Allows the field to be optional in forms
        null=True # Allows the database field to be nullable
    )

    bio = models.TextField(
        blank=True,
        null=True
    )
    

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"