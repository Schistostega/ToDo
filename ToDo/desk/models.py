from django.db.models import Model
from django.db.models.fields import CharField


class Project(Model):
    name = CharField(max_length=50)

    def __str__(self):
        return self.name
