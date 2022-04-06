from django.urls import path

from . import views

urlpatterns = [
    path('', views.news, name='news'),
    path('submit/', views.submit, name='submit'),
    path('newest/', views.newest, name='newest'),
    path('news/', views.news, name='news'),
    path('submitted=<username>', views.newsUser, name='newsUser'),
    path('date=<date>', views.newsDate, name='newsDate'),
    path('user/<username>/', views.user, name='user'),

]
