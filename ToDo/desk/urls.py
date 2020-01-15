from django.urls import path

from . import views

app_name = 'desk'
urlpatterns = [
    path('projects/create', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/update/<int:pk>', views.ProjectUpdateView.as_view(), name='project_update'),
    path('projects/delete/<int:pk>', views.ProjectDeleteView.as_view(), name='project_delete'),

    path('tasks/create', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/update/<int:pk>', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/delete/<int:pk>', views.TaskDeleteView.as_view(), name='task_delete'),

    path('set-timezone', views.set_timezone, name='set_timezone'),
]
