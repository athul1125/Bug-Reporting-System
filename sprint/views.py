from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.db.models import Avg, Sum, F, ExpressionWrapper, DurationField
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .models import *
from .forms import SprintForm

class NonTesterMixin(UserPassesTestMixin):
    """Mixin to prevent testers from accessing sprint views"""
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        return self.request.user.profile.role != 'tester'
    
    def handle_no_permission(self):
        raise PermissionDenied("Testers do not have access to sprint management.")

class SprintListView(NonTesterMixin, ListView):
    model = Sprint
    template_name = 'sprint/sprint_list.html'

class SprintDetailView(NonTesterMixin, DetailView):
    model = Sprint
    template_name = 'sprint/sprint_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sprint = self.get_object()
        bugs = sprint.bug_set.all()
        context['bugs'] = bugs

        from django.db.models import Case, When, Value
        from django.utils import timezone
        
        # Create a custom duration calculation based on status
        duration_case = Case(
            When(
                status__in=['Fixed', 'Closed'],
                then=ExpressionWrapper(
                    F('fixed_at') - F('in_progress_at'),
                    output_field=DurationField()
                )
            ),
            When(
                status='In Progress',
                then=ExpressionWrapper(
                    Value(timezone.now()) - F('in_progress_at'),
                    output_field=DurationField()
                )
            ),
            default=Value(None),
            output_field=DurationField(),
        )
        
        # Only include bugs that have been in progress or are fixed
        working_bugs = bugs.exclude(in_progress_at__isnull=True)
        working_bugs = working_bugs.annotate(working_duration=duration_case)

        # Calculate averages and totals for bugs that have been worked on
        context['platform_avg'] = working_bugs.values('platform').annotate(
            avg_duration=Avg('working_duration')
        ).exclude(avg_duration__isnull=True)

        context['developer_avg'] = working_bugs.values(
            'fixed_by', 'fixed_by__username'
        ).annotate(
            avg_duration=Avg('working_duration')
        ).exclude(avg_duration__isnull=True)

        context['developer_total'] = working_bugs.values(
            'fixed_by', 'fixed_by__username'
        ).annotate(
            total=Sum('working_duration')
        ).exclude(total__isnull=True)

        # Calculate sprint total work duration
        context['sprint_total'] = working_bugs.aggregate(
            total=Sum('working_duration')
        )['total']

        return context

class SprintCreateView(NonTesterMixin, CreateView):
    model = Sprint
    form_class = SprintForm
    template_name = 'sprint/sprint_form.html'
    success_url = reverse_lazy('sprint_list')

class SprintUpdateView(NonTesterMixin, UpdateView):
    model = Sprint
    form_class = SprintForm
    template_name = 'sprint/sprint_form.html'
    success_url = reverse_lazy('sprint_list')

class SprintDeleteView(NonTesterMixin, DeleteView):
    model = Sprint
    template_name = 'sprint/sprint_confirm_delete.html'
    success_url = reverse_lazy('sprint_list')

