import pytz
from django.views import generic
from django.shortcuts import render, redirect
from .models import Project


def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/desk/projects')  # !!!HARDCODE!!!
    else:
        return render(request, 'desk/tz_template.html', {'timezones': pytz.common_timezones})


class ProjectListView(generic.ListView):
    model = Project


class ProjectDetailView(generic.DetailView):
    model = Project


class ProjectUpdateView(generic.UpdateView):
    model = Project
    fields = ('name',)
