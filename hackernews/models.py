from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=15)
    karma = models.IntegerField(default=1)
    about = models.TextField(default="")
    email = models.EmailField(max_length=60)
    showdead = models.BooleanField()
    noprocrast = models.BooleanField()
    maxvisit = models.CharField(max_length=16) #integerField?
    minaway = models.CharField(max_length=16)
    delay = models.CharField(max_length=16)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

class Submission(models.Model):
    title = models.CharField(max_length=50, default="")
    url = models.URLField(max_length=50, default="")
    text = models.TextField(default="")
    type = models.CharField(default="url", max_length=3)
    points = models.IntegerField(default=0)
    author = models.CharField(default="", max_length=15)
    posted_at = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return self.title


#Change your models (in models.py).
#Run python manage.py makemigrations hackernews             to create migrations for those changes
#Run (optional) py manage.py sqlmigrate hackernews 000x     to check what would that migration make to the db
#Run python manage.py migrate                               to apply those changes to the database.
#https://docs.djangoproject.com/en/4.0/intro/tutorial02/
