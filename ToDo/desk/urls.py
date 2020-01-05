from django.urls import path

from . import views

app_name = 'desk'
urlpatterns = [
    path('projects', views.ProjectListView.as_view(), name='index'),
    path('projects/<int:pk>', views.ProjectUpdateView.as_view(), name='project_detail'),
    path('set-timezone', views.set_timezone, name='set_timezone'),
]
