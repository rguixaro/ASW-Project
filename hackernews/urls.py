from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('login/', TemplateView.as_view(template_name="login.html")),
    path('accounts/', include('allauth.urls')),
    path('logout/', LogoutView.as_view()),
    path('', views.news, name='main'),
    path('submit/', views.submit, name='submit'),
    path('newswelcome/', views.newsWelcome, name='newsWelcome'),
    path('newest/', views.newest, name='newest'),
    path('ask/', views.newest, name='ask'),
    path('news/', views.news, name='news'),
    #path('newcomments/', views.newcomments, name='newcomments'),
    #path('show/', views.show, name='show'),
    #path('front/', views.front, name='front'),
    #path('ask/', views.ask, name='ask'),
    #path('jobs/', views.jobs, name='jobs'),
    path('news/<date>', views.newsDate, name='newsDate'),
    path('<username>/', views.user, name='user'),
    path('<username>/submissions', views.newsUser, name='submissions'),
    path('<username>/threads', views.threads, name='threads'),
    path('<username>/upvoted', views.upvotedSubmissions, name='upvotedSubmissions'),
    path('<username>/upvoted&comments', views.upvotedComments, name='upvotedComments'),
]
