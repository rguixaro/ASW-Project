from django.db import models

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
    created_at = models.TextField(default="")

class Submission(models.Model):
    title = models.CharField(max_length=50, default="")
    url = models.URLField(max_length=50, default="")
    text = models.TextField(default="")


#Change your models (in models.py).
#Run python manage.py makemigrations to create migrations for those changes
#Run (optional) py manage.py sqlmigrate hackernews 000x 
#Run python manage.py migrate to apply those changes to the database.
#https://docs.djangoproject.com/en/4.0/intro/tutorial02/
