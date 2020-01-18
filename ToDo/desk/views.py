import pytz
from django.core.exceptions import PermissionDenied
from django.views import generic
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Project, Task
from .forms import ProjectForm, TaskForm


def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('desk:project_list')
    else:
        return render(request, 'desk/tz_template.html', {'timezones': pytz.common_timezones})


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'desk/form.html'
    extra_context = {'title': 'Project Create'}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['button_label'] = 'Create'
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    extra_context = {'title': 'Projects List'}

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'desk/form.html'
    extra_context = {'title': 'Project Update'}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['button_label'] = 'Update'
        return kwargs

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.user:
            return True
        else:
            return False


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy('desk:project_list')

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.user:
            return True
        else:
            return False


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'desk/form.html'
    extra_context = {'title': 'Task Create'}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['button_label'] = 'Create'
        return kwargs

    def form_valid(self, form):
        if form.instance.project.user == self.request.user:
            return super().form_valid(form)
        else:
            raise PermissionDenied


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'desk/form.html'
    extra_context = {'title': 'Task Update'}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['button_label'] = 'Update'
        return kwargs

    def test_func(self):
        task = self.get_object()
        project = task.project
        if self.request.user == project.user:
            return True
        else:
            return False


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy('desk:project_list')

    def test_func(self):
        task = self.get_object()
        project = task.project
        if self.request.user == project.user:
            return True
        else:
            return False
