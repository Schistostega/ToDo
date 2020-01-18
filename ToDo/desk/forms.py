from django import forms
from django.utils import timezone

from .models import Project, Task


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['date_created'] = forms.DateTimeField(initial=timezone.now)
        self.fields['project'].queryset = Project.objects.filter(user=user)

    class Meta:
        model = Task
        fields = ('title', 'description', 'date_created', 'project')
