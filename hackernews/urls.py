from django.urls import path

from . import views

urlpatterns = [
    path('', views.news, name='news'),
    path('submit/', views.submit, name='submit'),
    path('newest/', views.newest, name='newest'),
    path('news/', views.news, name='news'),
    path('newcomments/', views.newcomments, name='newcomments'),
    path('show/', views.show, name='show'),
    path('front/', views.front, name='front'),
    path('ask/', views.ask, name='ask'),
    path('jobs/', views.jobs, name='jobs'),
    path('news/<date>', views.newsDate, name='newsDate'),
    path('users/<username>/', views.user, name='user'),
    path('users/<username>/favorites', views.favorites, name='favorites'),
    path('users/<username>/submissions', views.newsUser, name='newsUser'),
    path('users/<username>/<date>', views.newsByDate, name='newsByDate'),
]
