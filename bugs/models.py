from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from sprint.models import *
from django.utils import timezone

class Bug(models.Model):
    
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Fixed', 'Fixed'),
        ('Closed', 'Closed'),
    ]

    platform_choices = [
        ('windows', 'Windows'), 
        ('web', 'Web'), 
        ('ios', 'iOS')
    ]

    class Meta:
        permissions = [
            ('Can change status', 'Can change status'),
        ]

    bugcode = models.CharField(max_length=10, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.TextField()
    screenshot = models.ImageField(upload_to='screenshots/')
    created_by = models.CharField(max_length=100, editable = False)
    contact_number = models.CharField(
        max_length = 15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    in_progress_at = models.DateTimeField(null=True, blank=True)
    fixed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='bug_updater')
    fixed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='bug_fixer')
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=platform_choices)

    def save(self, *args, **kwargs):
        if not self.bugcode:
            last_bug = Bug.objects.order_by('id').last()
            next_id = 1 if not last_bug else last_bug.id + 1
            self.bugcode = f'BUG{next_id:03d}'
        
        if self.pk:  # If this is an update, not a new bug
            old_bug = Bug.objects.get(pk=self.pk)
            if old_bug.status != 'In Progress' and self.status == 'In Progress':
                self.in_progress_at = timezone.now()
            elif old_bug.status != 'Fixed' and self.status == 'Fixed':
                self.fixed_at = timezone.now()
        elif self.status == 'In Progress':  # New bug being created with In Progress status
            self.in_progress_at = timezone.now()
            
        super().save(*args, **kwargs)

    @property
    def duration(self):
        if self.created_at and self.updated_at:
            return (self.updated_at - self.created_at).total_seconds() // 60 //60
        return None

    @property
    def duration_in_hours(self):
        if self.created_at and self.updated_at:
            return (self.updated_at - self.created_at).total_seconds() / 3600
        return 0

    @property
    def working_duration(self):
        """Calculate working duration based on status"""
        if not self.in_progress_at:
            return None
            
        if self.status in ['Fixed', 'Closed']:
            # For fixed/closed bugs, calculate time from in_progress until fixed
            if self.fixed_at:
                return self.fixed_at - self.in_progress_at
            return None
        elif self.status == 'In Progress':
            # For in-progress bugs, calculate time until now
            return timezone.now() - self.in_progress_at
        return None

    def __str__(self):
        return f"Bug #{self.id} - {self.status}"
