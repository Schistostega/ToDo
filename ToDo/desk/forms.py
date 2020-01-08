from django import forms
from django.utils import timezone

from .models import Project, Task


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', )


class TaskForm(forms.ModelForm):
    date_created = forms.DateTimeField(initial=timezone.now)

    class Meta:
        model = Task
        fields = ('title', 'description', 'date_created', 'project')
