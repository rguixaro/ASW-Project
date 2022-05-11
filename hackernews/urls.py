from django.urls import path, include
from django.contrib.auth.views import LogoutView

from . import views, api

urlpatterns = [
    path('login/', views.login, name='login'),
    path('accounts/', include('allauth.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.news, name='main'),
    path('submit/', views.submit, name='submit'),
    path('newswelcome/', views.newsWelcome, name='newsWelcome'),
    path('newest/', views.newest, name='newest'),
    path('ask/', views.ask, name='ask'),
    path('news/', views.news, name='news'),
    path('news/<date>', views.newsDate, name='newsDate'),
    path('vote/<submission_id>', views.upvote, name='upvote'),
    path('unvote/<submission_id>', views.unvote, name='unvote'),
    path('news/vote/<submission_id>', views.upvote, name='upvote'),
    path('news/unvote/<submission_id>', views.unvote, name='unvote'),
    path('newest/vote/<submission_id>', views.upvote, name='upvote'), #treure?
    path('item/<submission_id>/comments', views.comments, name='comments'),
    path('<username>/', views.user, name='user'),
    path('<username>/submissions', views.newsUser, name='submissions'),
    path('<username>/threads', views.threads, name='threads'),
    path('<username>/upvoted', views.upvotedSubmissions, name='upvotedSubmissions'),
    path('<username>/upvoted&comments', views.upvotedComments, name='upvotedComments'),
    path('item/<submission_id>', views.detailedSubmission, name='detailedSubmission'),
    path('reply/<comment_id>', views.reply, name='reply'),
    path('api/<username>/submissions', api.newsUser, name='api-submissions'),
    path('api/submission', api.submission, name='api-Submission'),
    path('api/<username>', api.user, name='api-user'),
    path('api/submission/<submission_id>', api.detailedSubmission, name='api-detailedSubmission'),
    path('api/date/<date>', api.dateSubmissions, name='api-dateSubmissions')


]
