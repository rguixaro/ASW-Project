from django.urls import path

from . import views

urlpatterns = [
    path('', views.news, name='news'),
    path('submit/', views.submit, name='submit'),
    path('newswelcome/', views.newsWelcome, name='newsWelcome'),
    path('newest/', views.newest, name='newest'),
    path('ask/', views.newest, name='ask'),
    path('news/', views.news, name='news'),
    path('news/<date>', views.newsDate, name='newsDate'),
    path('user/<username>/', views.user, name='user'),
    path('users/<username>/', views.user, name='user'),
    path('users/<username>/submissions', views.newsUser, name='submissions'),
    path('users/<username>/threads', views.threads, name='threads'),
    path('users/<username>/favorites', views.favorites, name='favorites'),
]
