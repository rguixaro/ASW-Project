from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from hackernews.models import Submission, User
from .forms import SubmitForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def submit(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SubmitForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            newest()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SubmitForm()

    return render(request, "submit.html", {'form': form})


def newcomments(request):
    return render(request, "submit.html")


def show(request):
    return render(request, "submit.html")


def front(request):
    return render(request, "submit.html")


def ask(request):
    return render(request, "submit.html")


def jobs(request):
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

def newsByDate(request, date, username):
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

def favorites(request, username):
    u = User.objects.get(username=username)
    template = loader.get_template('favorites.html')
    context = {
        'user' : u,
    }
    return HttpResponse(template.render(context, request))
