from django.db.models import Model
from django.db.models.fields import CharField
from django.urls import reverse


class Project(Model):
    name = CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('desk:project_detail', kwargs={'pk': self.id})
