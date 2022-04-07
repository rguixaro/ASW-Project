from django.contrib import admin

from .models import Submission, User, Comment

# Register your models here.

admin.site.register(Submission)
admin.site.register(User)
admin.site.register(Comment)

