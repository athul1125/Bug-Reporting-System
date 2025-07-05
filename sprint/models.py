from django.db import models
from django.contrib.auth.models import User

class Sprint(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField(default=14)
    lead_developer = models.ForeignKey(User, related_name='lead_sprints', on_delete=models.CASCADE)
    developers = models.ManyToManyField(User, related_name='sprints')

    def get_bug_counts(self):
        """Returns a dictionary with counts of bugs in different states"""
        bugs = self.bug_set.all()
        return {
            'total': bugs.count(),
            'open': bugs.filter(status='Open').count(),
            'in_progress': bugs.filter(status='In Progress').count(),
            'fixed': bugs.filter(status='Fixed').count(),
            'closed': bugs.filter(status='Closed').count(),
        }

    def get_active_developers(self):
        """Returns count of developers with assigned bugs"""
        return self.bug_set.values('fixed_by').distinct().exclude(fixed_by__isnull=True).count()

    def __str__(self):
        return self.name