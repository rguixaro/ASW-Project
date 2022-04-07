from django.db import models
from django.utils import timezone
from datetime import date, datetime

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
    created_at_date = models.DateField(default=timezone.now)
    created_at_time = models.TimeField(default=timezone.now)

    def age(self):
        today = date.today()
        days = today.day - self.created_at_date.day
        result = str(days)+" days ago"
        if(days == 0):
            time = datetime.now()
            hours = time.hour - self.created_at_time.hour
            result = str(hours)+" hours ago"
        #check days, weeks, etc...
        return result

    def __str__(self):
        return self.username

class Submission(models.Model):
    title = models.CharField(max_length=50, default="")
    url = models.URLField(max_length=50, default="")
    text = models.TextField(default="")
    type = models.CharField(default="url", max_length=3)
    points = models.IntegerField(default=0)
    author = models.CharField(default="", max_length=15)
    comments = models.IntegerField(default=0)
    posted_at_date = models.DateField(default=timezone.now)
    posted_at_time = models.TimeField(default=timezone.now)
    
    def url_domain(self):
        return (self.url).replace('https://www.','')

    def age(self):
        today = date.today()
        days = today.day - self.posted_at_date.day
        result = str(days)+" days ago"
        if(days == 0):
            time = datetime.now()
            hours = time.hour - self.posted_at_time.hour
            result = str(hours)+" hours ago"
        #check days, weeks, etc...
        return result

    def __str__(self):
        return self.title


#Change your models (in models.py).
#Run python manage.py makemigrations hackernews             to create migrations for those changes
#Run (optional) py manage.py sqlmigrate hackernews 000x     to check what would that migration make to the db
#Run python manage.py migrate                               to apply those changes to the database.
#https://docs.djangoproject.com/en/4.0/intro/tutorial02/
