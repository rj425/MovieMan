from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth.models import User


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Task(models.Model):

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, to_field='username', default='Anonymous')
    imdbUrl = models.URLField(max_length=200, null=False, blank=False)
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
    rating = models.FloatField(null=False)
    numRatings = models.PositiveIntegerField(null=False)
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.year)


class Cast(models.Model):

    id = models.AutoField(primary_key=True)
    movieId = models.ForeignKey(Movie, on_delete=models.PROTECT)
    star = models.CharField(max_length=100, null=False)
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.star)


class Activity(models.Model):

    WATCH = 'WATCH'
    WATCHED = 'WATCHED'

    ACTION_CHOICES = (
        (WATCH, 'WATCHED'),
        (WATCHED, 'WATCH')
    )

    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(
        User, on_delete=models.PROTECT, to_field='username')
    movieId = models.ForeignKey(Movie, on_delete=models.PROTECT)
    action = models.CharField(
        max_length=10, choices=ACTION_CHOICES, null=False, blank=False)
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}, {}, {}'.format(self.username, self.movieId, self.action)

    class Meta:
        unique_together = ('username', 'movieId')
