from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, to_field='username')
    url = models.URLField(max_length=200, null=False, blank=False)
    movieCount = models.PositiveIntegerField(default=0)
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Task-{}".format(self.id)


class Movie(models.Model):

    id = models.AutoField(primary_key=True)
    taskId = models.ForeignKey(Task, on_delete=models.PROTECT)
    name = models.CharField(max_length=200, unique=True, null=False)
    year = models.PositiveIntegerField(null=False)
    director = models.CharField(max_length=100, null=False)
    link = models.URLField(max_length=200, null=False)
    rating = models.FloatField()
    numRatings = models.PositiveIntegerField()
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.year)


class Cast(models.Model):

    id = models.AutoField(primary_key=True)
    movieId = models.ForeignKey(Movie, on_delete=models.PROTECT)
    star = models.CharField(max_length=100)
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.star)
