import pytz
from django.views import generic
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Project, Task
from .forms import ProjectForm, TaskForm


def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/desk/projects')  # !!!HARDCODE!!!
    else:
        return render(request, 'desk/tz_template.html', {'timezones': pytz.common_timezones})


class ProjectCreateView(generic.CreateView):
    model = Project
    form_class = ProjectForm
    extra_context = {'title': 'Project Create'}


class ProjectListView(generic.ListView):
    model = Project
    extra_context = {'title': 'Projects List'}


class ProjectUpdateView(generic.UpdateView):
    model = Project
    form_class = ProjectForm
    extra_context = {'title': 'Project Update'}
    template_name_suffix = '_update_form'


class ProjectDeleteView(generic.DeleteView):
    model = Project
    success_url = reverse_lazy('desk:project_list')


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    extra_context = {'title': 'Task Create'}


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    extra_context = {'title': 'Task Update'}
    template_name_suffix = '_update_form'


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy('desk:project_list')
