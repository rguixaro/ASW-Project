from django.db import models

# Create your models here.


class Submission(models.Model):
    title = models.CharField(max_length=50, default="")
    url = models.CharField(max_length=50, default="")
    text = models.CharField(max_length=200, default="", null=True)
