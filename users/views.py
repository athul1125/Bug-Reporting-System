from django.views.generic import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from .models import *
from .forms import ProfileForm, CustomUserCreationForm

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'

@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'users.edit_user_profile_perm'
    raise_exception = True
    model = Profile
    form_class = ProfileForm
    template_name = 'profile_form.html'
    success_url = reverse_lazy('bug-list')

    def get_object(self):
        return self.request.user.profile
    
@method_decorator(login_required, name='dispatch')
class ProfileDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'users.view_profile'
    raise_exception = True
    model = Profile
    template_name = 'profile_detail.html'

    def get_object(self):
        return self.request.user.profile

@method_decorator(login_required, name='dispatch')
class UserRegisterView(PermissionRequiredMixin, CreateView):
    permission_required = 'users.add_profile'
    raise_exception = True
    form_class = CustomUserCreationForm
    template_name = 'create_user.html'
    success_url = reverse_lazy('bug-list')

class UserEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'auth.change_user'
    model = User
    form_class = CustomUserCreationForm
    template_name = 'user_edit.html'
    success_url = reverse_lazy('user-list')

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.kwargs['pk'])

class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'auth.delete_user'
    model = User
    template_name = 'user_delete.html'
    success_url = reverse_lazy('user-list')

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.kwargs['pk'])