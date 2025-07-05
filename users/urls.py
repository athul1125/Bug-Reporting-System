from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('list/', UserListView.as_view(), name='user-list'),
    path('create/', UserRegisterView.as_view(), name='create'),
    path('profile/', ProfileDetailView.as_view(), name='profile-view'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile-edit'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('edit/<int:pk>/', UserEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='delete'),
]