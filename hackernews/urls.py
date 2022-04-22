from django.urls import path, include
from django.contrib.auth.views import LogoutView

from . import views

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
    path('news/vote/<submission_id>', views.upvote, name='upvote'),
    path('newest/vote/<submission_id>', views.upvote, name='upvote'),
    path('item/<submission_id>/comments', views.comments, name='comments'),
    path('<username>/', views.user, name='user'),
    path('<username>/submissions', views.newsUser, name='submissions'),
    path('<username>/threads', views.threads, name='threads'),
    path('<username>/upvoted', views.upvotedSubmissions, name='upvotedSubmissions'),
    path('<username>/upvoted&comments', views.upvotedComments, name='upvotedComments'),
    path('item/<submission_id>', views.detailedSubmission, name='detailedSubmission'),

]
