from django.urls import path
from .views import SprintDetailView, SprintCreateView, SprintUpdateView, SprintDeleteView, SprintListView

urlpatterns = [
    path('', SprintListView.as_view(), name='sprint_list'),
    path('<int:pk>/', SprintDetailView.as_view(), name='sprint_detail'),
    path('create/', SprintCreateView.as_view(), name='sprint_create'),
    path('<int:pk>/update/', SprintUpdateView.as_view(), name='sprint_update'),
    path('<int:pk>/delete/', SprintDeleteView.as_view(), name='sprint_delete'),
]