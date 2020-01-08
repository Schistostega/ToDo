from django.db.models import Model, ForeignKey, CASCADE
from django.db.models.fields import CharField, DateTimeField, TextField
from django.urls import reverse


class Project(Model):
    name = CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('desk:project_detail', kwargs={'pk': self.id})


class Task(Model):
    title = CharField(max_length=70)
    description = TextField()
    date_created = DateTimeField('date_created')
    project = ForeignKey(Project, on_delete=CASCADE)

    def __str__(self):
        return f'{self.title}, created: {self.date_created}, along to: {self.project}'

    def get_absolute_url(self):
        return reverse('desk:task_detail', kwargs={'pk': self.id})
