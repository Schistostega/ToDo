from django.views import generic
from .models import Project


class ProjectListView(generic.ListView):
    model = Project


class ProjectDetailView(generic.DetailView):
    model = Project


class ProjectUpdateView(generic.UpdateView):
    model = Project
    fields = ('name',)
