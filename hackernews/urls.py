from django.urls import path

from . import views

urlpatterns = [
    path('', views.news, name='news'),
    path('submit/', views.submit, name='submit'),
    path('newest/', views.newest, name='newest'),
    path('news/', views.news, name='news'),
    path('news/<username>/', views.newsUser, name='news-user'),
    path('news/<date>/', views.newsDate, name='news-date'),
    path('user/<username>/', views.user, name='user'),

]
