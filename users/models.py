from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('developer', 'Developer'),
        ('tester', 'Tester'),
    ]

    class Meta:
        permissions = [
            ('edit_user_profile_perm', 'Can edit user profile')
        ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    contact_number = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    