from django.urls import path
from .views import *

urlpatterns = [
    path('', BugListView.as_view(), name='bug-list'),
    path('bug/<int:pk>/', BugDetailView.as_view(), name='bug-detail'),
    path('bug/<int:pk>/edit/', BugUpdateFormView.as_view(), name='bug-edit'),
    path('bug/<int:pk>/status/', BugStatusUpdateView.as_view(), name='bug-status'),
    path('bug/<int:pk>/delete/', BugDeleteFormView.as_view(), name='bug-delete'),
    path('report/', BugCreateFormView.as_view(), name='bug-create'),
    path('download/', download_bugs_excel, name='bug-download'),
    path('upload/', upload_bugs_excel, name='bug-upload'),
    path('developer-stats/', DeveloperStatsView.as_view(), name='developer-stats'),
    path('api/developer-stats/', DeveloperStatsAPIView.as_view(), name='api-developer-stats'),
    path('my-bugs/', MyBugsListView.as_view(), name='my-bugs'),
    path('my-assigned-bugs/', MyAssignedBugsListView.as_view(), name='my-assigned-bugs'),
]