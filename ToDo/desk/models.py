from django.db.models import Model, ForeignKey, CASCADE
from django.db.models.fields import CharField, DateTimeField, TextField
from django.contrib.auth.models import User
from django.urls import reverse


class Project(Model):
    name = CharField(max_length=50)
    user = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return self.name

    @staticmethod
    def get_absolute_url():
        return reverse('desk:project_list')


class Task(Model):
    title = CharField(max_length=70)
    description = TextField()
    date_created = DateTimeField('date_created')
    project = ForeignKey(Project, on_delete=CASCADE)

    def __str__(self):
        return f'{self.title}, created: {self.date_created}'

    @staticmethod
    def get_absolute_url():
        return reverse('desk:project_list')
