from django.db.models import Model, ForeignKey, CASCADE
from django.db.models.fields import CharField, DateTimeField, TextField, SmallIntegerField
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Project(Model):
    name = CharField(max_length=50)
    user = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return self.name

    @staticmethod
    def get_absolute_url():
        return reverse('desk:project_list')


class Task(Model):
    STATUS = ((0, 'new'),
              (1, 'in_progress'),
              (2, 'wasted'),
              (3, 'done'))

    title = CharField(max_length=70)
    description = TextField()
    date_created = DateTimeField('date_created')
    deadline = DateTimeField('deadline', null=True, blank=True)
    status = SmallIntegerField(choices=STATUS, default=0)
    project = ForeignKey(Project, on_delete=CASCADE)

    def __str__(self):
        return f'{self.title}, created: {self.date_created}'

    def update_status(self):
        if self.status != 3:  # if status is not done -- check for update
            if self.deadline and self.status == 0:
                print('case_1')
                self.status = 1
                self.save()
            elif not self.deadline and self.status != 0:
                print('case_2')
                self.status = 0
                self.save()
            elif self.deadline:
                timedelta = self.deadline - timezone.now()
                if timedelta.days < 0 and self.status != 2:
                    print('case_3')
                    self.status = 2
                    self.save()
                elif timedelta.days >= 0 and self.status != 1:
                    print('case_4')
                    self.status = 1
                    self.save()
            return self.get_time_to_deadline()
        else:
            return None

    def get_time_to_deadline(self):
        """
        Func returns time to deadline as a string.
        """
        timedelta = self.deadline - timezone.now()
        if timedelta.days < 0:
            return f'0 seconds'
        elif timedelta.days >= 1:
            return f'{timedelta.days} days'
        elif timedelta.days <= 0 and timedelta.seconds > 3600:  # more than an hour
            return f'{timedelta.seconds // 3600} hours'
        elif timedelta.seconds < 3600:
            return f'{timedelta.seconds // 60} minutes'
        elif timedelta.seconds < 60:
            return f'{timedelta.seconds} seconds'

    @staticmethod
    def get_absolute_url():
        return reverse('desk:project_list')
