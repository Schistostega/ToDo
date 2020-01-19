import pytz
from django.core.exceptions import PermissionDenied
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

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
        """
        Function to send extra args to the form
        """
        kwargs = super().get_form_kwargs()
        kwargs['button_label'] = 'Create'
        kwargs['form_legend'] = 'Enter a name for the new project'
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
        """
        Function to send extra args to the form
        """
        kwargs = super().get_form_kwargs()
        kwargs['button_label'] = 'Update'
        kwargs['form_legend'] = 'Enter new name for the project'
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
        """
        Function to send extra args to the form
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['button_label'] = 'Create'
        kwargs['form_legend'] = 'Creating Task Form.'
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
        """
        Function to send extra args to the form
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['button_label'] = 'Update'
        kwargs['form_legend'] = 'Updating Task Form.'
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


@login_required
def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = 3
    task.save()
    messages.success(request, f'Task has been marked as done.')
    return redirect('desk:project_list')
