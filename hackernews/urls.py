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
    #path('users/<username>/', views.user, name='user'),
    #path('users/<username>/favorites', views.favorites, name='favorites'),
    #path('users/<username>/submissions', views.newsUser, name='newsUser'),
    #path('users/<username>/<date>', views.newsByDate, name='newsByDate'),
    path('vote?id=<submission_id>&how=up&goto=news', views.upvote, name='upvote'),
    path('<username>/', views.user, name='user'),
    path('<username>/submissions', views.newsUser, name='submissions'),
    path('<username>/threads', views.threads, name='threads'),
    path('<username>/upvoted', views.upvotedSubmissions, name='upvotedSubmissions'),
    path('<username>/upvoted&comments', views.upvotedComments, name='upvotedComments'),
]
