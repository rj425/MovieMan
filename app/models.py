from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, to_field='username')
    url = models.URLField(max_length=200, null=False, blank=False)
    movieCount = models.PositiveIntegerField(default=0)
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Task-{}".format(self.id)
