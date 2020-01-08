import pytz
from django.views import generic
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Project
from .forms import ProjectForm


def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/desk/projects')  # !!!HARDCODE!!!
    else:
        return render(request, 'desk/tz_template.html', {'timezones': pytz.common_timezones})


class ProjectListView(generic.ListView):
    model = Project
    extra_context = {'title': 'Projects List'}


class ProjectDetailView(generic.DetailView):
    model = Project
    extra_context = {'title': 'Projects Detail'}


class ProjectCreateView(generic.CreateView):
    model = Project
    form_class = ProjectForm
    extra_context = {'title': 'Projects Create'}


class ProjectUpdateView(generic.UpdateView):
    model = Project
    form_class = ProjectForm
    extra_context = {'title': 'Projects Update'}
    template_name_suffix = '_update_form'


class ProjectDeleteView(generic.DeleteView):
    model = Project
    success_url = reverse_lazy('desk:project_list')
