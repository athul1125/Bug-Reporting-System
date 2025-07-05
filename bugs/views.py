from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden, HttpResponse
from django.utils.decorators import method_decorator
from users.decorators import *
from .models import *
from .forms import *
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import DeveloperStatsSerializer
from rest_framework.permissions import IsAuthenticated

class BugListView(LoginRequiredMixin, ListView):
    model = Bug
    template_name = 'bugs/bug_list.html'
    context_object_name = 'bugs'

class BugDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'bugs.view_bug'
    raise_exception = True
    model = Bug
    template_name = 'bugs/bug_detail.html'
    context_object_name = 'bug'

class BugCreateFormView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = 'bugs.add_bug'
    raise_exception = True
    form_class = BugForm
    template_name = 'bugs/bug_form.html'
    success_url = reverse_lazy('bug-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_role'] = self.request.user.profile.role
        return kwargs

    def form_valid(self, form):
        bug = form.save(commit=False)
        bug.created_by = self.request.user
        bug.user = self.request.user
        bug.contact_number = self.request.user.profile.contact_number
        if self.request.user.profile.role == 'tester':
            # Assign the latest sprint by default for testers
            latest_sprint = Sprint.objects.order_by('-id').first()
            if latest_sprint:
                bug.sprint = latest_sprint
            else:
                # Handle the case where no sprints exist if necessary
                # For now, this will cause an error if no sprints are available
                # which is reasonable.
                pass
        bug.save()
        form.save_m2m()
        return redirect(self.success_url)


class BugUpdateFormView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'bugs.change_bug'
    raise_exception = True
    model = Bug
    form_class = BugForm
    template_name = 'bugs/bug_form.html'
    success_url = reverse_lazy('bug-list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            return HttpResponseForbidden("You are not allowed to edit this bug. ")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_role'] = self.request.user.profile.role
        return kwargs

    def form_valid(self, form):
        bug = form.save(commit=False)
        if self.request.user.profile.role == 'developer':
            bug.fixed_by = self.request.user
        bug.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Update {self.object.bugcode}'
        return context
    
class BugDeleteFormView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'bugs.delete_bug'
    raise_exception = True
    model = Bug
    template_name = 'bugs/bug_confirm_delete.html'
    success_url = reverse_lazy('bug-list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            return HttpResponseForbidden("You are not allowed to delete this bug. ")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Delete Bug #{self.object.pk}'
        return context
    
#@method_decorator(has_bug_status_permission, name='dispatch')
class BugStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Bug
    form_class = BugForm
    template_name = 'bugs/bug_form.html'
    success_url = reverse_lazy('bug-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_role'] = self.request.user.profile.role
        return kwargs

    def form_valid(self, form):
        bug = form.save(commit=False)
        if self.request.user.profile.role == 'developer':
            bug.updated_by = self.request.user
            if bug.status == 'Fixed':
                bug.fixed_by = self.request.user
        bug.save()
        messages.success(self.request, 'Bug status updated successfully.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Update Status for {self.object.bugcode}"
        return context
    
def download_bugs_excel(request):
    bugs = Bug.objects.all().values('bugcode', 'status', 'created_by', 'contact_number', 'created_at', 'updated_at')
    df = pd.DataFrame(list(bugs))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheeetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=bug_report.xlsx'

    for col in df.select_dtypes(include=['datetimetz']).columns:
        df[col] = df[col].dt.tz_localize(None)

    df.to_excel(response, index=False)
    return response

def  upload_bugs_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            try:
                df = pd.read_excel(excel_file)

                updated_count = 0
                for _, row in df.iterrows():
                    bugcode = str(row.get('bugcode')).strip()
                    st = ['Open', 'In Progress', 'Fixed', 'Closed']
                    status = str(row.get('status')).strip()
                    fixed_by_from_excel = row.get('fixed_by')
                    if pd.isna(fixed_by_from_excel):
                        fixed_by_from_excel = ''
                    else:
                        fixed_by_from_excel = str(fixed_by_from_excel).strip()

                    if bugcode and status:
                        try:
                            bug = Bug.objects.get(bugcode=bugcode)
                            if bug.status != status and status in st:
                                bug.status = status
                                bug.updated_by = request.user
                                if status == 'Fixed':
                                    if fixed_by_from_excel:
                                        try:
                                            user = User.objects.get(username=fixed_by_from_excel)
                                            bug.fixed_by = user
                                        except User.DoesNotExist:
                                            # If user not found, use current user
                                            bug.fixed_by = request.user
                                    else:
                                        bug.fixed_by = request.user
                                bug.save()
                                updated_count += 1
                            else:
                                continue
                        except Bug.DoesNotExist:
                            continue
                messages.success(request, f"{updated_count} bugs updated successfully.")
            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
            return redirect('bug-list')
    else:
        form = ExcelUploadForm()
    return render(request, 'bugs/excel_upload.html', {'form': form})

class DeveloperStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        developers = User.objects.filter(profile__role='developer')
        serializer = DeveloperStatsSerializer(developers, many=True)
        return Response(serializer.data)

class DeveloperStatsView(LoginRequiredMixin, TemplateView):
    template_name = 'bugs/developer_stats.html'
    '''
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.groups.filter(name='tester').exists()):
            return HttpResponseForbidden("You are not allowed to view this page.")
        return super().dispatch(request, *args, **kwargs)
    '''

class MyBugsListView(LoginRequiredMixin, ListView):
    model = Bug
    template_name = 'bugs/my_bugs.html'
    context_object_name = 'bugs'

    def get_queryset(self):
        return Bug.objects.filter(user=self.request.user).order_by('created_at')

class MyAssignedBugsListView(LoginRequiredMixin, ListView):
    model = Bug
    template_name = 'bugs/my_assigned_bugs.html'
    context_object_name = 'bugs'

    def get_queryset(self):
        return Bug.objects.filter(fixed_by=self.request.user).order_by('created_at')