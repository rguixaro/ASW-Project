from statistics import mode
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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
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

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    posted_at_date = models.DateField(default=timezone.now)
    posted_at_time = models.TimeField(default=timezone.now)
    text = models.TextField(default="")
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    @property
    def comment_id(self):
        return self.id

    def get_root(self):
        comment = self
        while comment.parent is not None:
            comment = comment.parent
        return comment.comment_id

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

#Change your models (in models.py).
#Run python manage.py makemigrations hackernews             to create migrations for those changes
#Run (optional) py manage.py sqlmigrate hackernews 000x     to check what would that migration make to the db
#Run python manage.py migrate                               to apply those changes to the database.
#https://docs.djangoproject.com/en/4.0/intro/tutorial02/
