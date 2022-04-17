from django.urls import path

from . import views

urlpatterns = [
    path('', views.news, name='main'),
    path('submit/', views.submit, name='submit'),
    path('newswelcome/', views.newsWelcome, name='newsWelcome'),
    path('newest/', views.newest, name='newest'),
    path('ask/', views.newest, name='ask'),
    path('news/', views.news, name='news'),
    path('news/<date>', views.newsDate, name='newsDate'),
    path('<username>/', views.user, name='user'),
    path('<username>/submissions', views.newsUser, name='submissions'),
    path('<username>/threads', views.threads, name='threads'),
    path('<username>/upvoted', views.upvoted, name='upvoted'),
]
