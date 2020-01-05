from django.urls import path

from . import views

app_name = 'desk'
urlpatterns = [
    path('projects/create', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/update/<int:pk>', views.ProjectUpdateView.as_view(), name='project_update'),
    path('projects/delete/<int:pk>', views.ProjectDeleteView.as_view(), name='project_delete'),
]
