from pyexpat import model
from statistics import mode
from django.db import models
from django.utils import timezone
from datetime import date, datetime
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User as AuthUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class User(models.Model):
    authUser = models.OneToOneField(AuthUser, on_delete=models.CASCADE, null=True)
    karma = models.IntegerField(default=1)
    about = models.TextField(default="")
    showdead = models.BooleanField(default=False)
    noprocrast = models.BooleanField(default=False)
    maxvisit = models.CharField(max_length=16, default=0) #integerField?
    minaway = models.CharField(max_length=16,default=0)
    delay = models.CharField(max_length=16,default=0)
    created_at_date = models.DateField(default=timezone.now)
    created_at_time = models.TimeField(default=timezone.now)

    @receiver(post_save, sender=AuthUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            User.objects.create(authUser = instance)

    @receiver(post_save, sender=AuthUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.user.save()

    def age(self):
        today = date.today()
        days = today.day - self.created_at_date.day
        result = str(days)+" days ago"
        if(days == 0):
            time = timezone.now()
            hours = time.hour - self.created_at_time.hour
            result = str(hours)+" hours ago"
            if (hours == 0):
                time = timezone.now()
                hours = time.minute - self.created_at_time.minute
                result = str(hours) + " minutes ago"
        return result

    def __str__(self):
        return self.authUser.username

class Action(models.Model):
    UPVOTE_SUBMISSION = 'US'
    UNVOTE_SUBMISSION = 'DS'
    UPVOTE_COMMENT = 'UC'
    UNVOTE_COMMENT = 'DC'
    ACTION_TYPES = (
        (UPVOTE_SUBMISSION, 'Upvote submission'),
        (UNVOTE_SUBMISSION, 'Unvote submission'),
        (UPVOTE_COMMENT, 'Upvote comment'),
        (UNVOTE_COMMENT, 'Unvote comment'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=2, choices=ACTION_TYPES)
    date = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

class Submission(models.Model):
    title = models.CharField(max_length=50, default="")
    url = models.URLField(max_length=50, default="")
    text = models.TextField(default="")
    type = models.CharField(default="url", max_length=3)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_at_date = models.DateField(default=timezone.now)
    posted_at_time = models.TimeField(default=timezone.now)
    upvotes = GenericRelation(Action)
    
    def url_domain(self):
        return (self.url).replace('https://www.','')

    def age(self):
        today = date.today()
        days = today.day - self.posted_at_date.day
        result = str(days) + " days ago"
        if (days == 0):
            time = timezone.now()
            hours = time.hour - self.posted_at_time.hour
            result = str(hours) + " hours ago"
            if (hours == 0):
                time = timezone.now()
                hours = time.minute - self.posted_at_time.minute
                result = str(hours) + " minutes ago"
        return result

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    posted_at_date = models.DateField(default=timezone.now)
    posted_at_time = models.TimeField(default=timezone.now)
    text = models.TextField(default="")
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    upvotes = GenericRelation(Action)

class Meta:
    ordering = ('-posted_at_date', '-posted_at_time')

    def _str_(self):
        return self.comment_id

    @property
    def comment_id(self):
        return self.id

    def root(self):
        root = self.get_root()
        return root.comment_id

    def descendant_count(self):
        return self.get_descendant_count()+1

    def age(self):
        today = date.today()
        days = today.day - self.posted_at_date.day
        result = str(days)+" days ago"
        if(days == 0):
            time = timezone.now()
            hours = time.hour - self.posted_at_time.hour
            result = str(hours)+" hours ago"
            if (hours == 0):
                time = timezone.now()
                hours = time.minute - self.posted_at_time.minute
                result = str(hours) + " minutes ago"
        return result


    


#Change your models (in models.py).
#Run python manage.py makemigrations hackernews             to create migrations for those changes
#Run (optional) py manage.py sqlmigrate hackernews 000x     to check what would that migration make to the db
#Run python manage.py migrate                               to apply those changes to the database.
#https://docs.djangoproject.com/en/4.0/intro/tutorial02/
