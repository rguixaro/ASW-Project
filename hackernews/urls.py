from django.urls import path

from . import views

urlpatterns = [
    path('', views.news, name='news'),
    path('submit/', views.submit, name='submit'),
    path('newest/', views.newest, name='newest'),
    path('ask/', views.newest, name='ask'),
    path('news/', views.news, name='news'),
    path('news/<date>', views.newsDate, name='newsDate'),
    path('users/<username>/', views.user, name='user'),
    path('users/<username>/favorites', views.favorites, name='favorites'),
    path('users/<username>/submissions', views.newsUser, name='newsUser'),
    path('users/<username>/<date>', views.newsByDate, name='newsByDate'),
]
