from django.contrib import admin
from app import models

admin.site.register(models.Task)
admin.site.register(models.Movie)
admin.site.register(models.Cast)
admin.site.register(models.Activity)