from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from hackernews.models import Submission, User


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def submit(request):
    return render(request, "submit.html")


def news(request):
    submissions_list = Submission.objects.order_by('-points')
    template = loader.get_template('news.html')
    context = {
        'submissions_list' : submissions_list,
    }
    return HttpResponse(template.render(context, request))

def newsUser(request, username):
    submissions_list = Submission.objects.filter(author=username)
    template = loader.get_template('news.html')
    context = {
        'submissions_list' : submissions_list,
    }
    return HttpResponse(template.render(context, request))

def newsDate(request, date):
    submissions_list = Submission.objects.filter(posted_at_date=date)
    template = loader.get_template('news.html')
    context = {
        'submissions_list' : submissions_list,
    }
    return HttpResponse(template.render(context, request))


def newest(request):
    return render(request, "newest.html")

def user(request, username):
    u = User.objects.get(username=username)
    template = loader.get_template('user.html')
    context = {
        'user' : u,
    }
    return HttpResponse(template.render(context, request))
