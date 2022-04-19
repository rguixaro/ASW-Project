from django.contrib import admin

from .models import Submission, User, Comment, Action
from mptt.admin import MPTTModelAdmin

# Register your models here.

admin.site.register(Submission)
admin.site.register(User)
admin.site.register(Comment, MPTTModelAdmin)
admin.site.register(Action)

