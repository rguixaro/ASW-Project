from django.http import HttpResponse
from django.shortcuts import render

from hackernews.models import Submission


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def submit(request):
    return render(request, "submit.html")


def news(request):
    #shows submissions with id=1
    #submissions = Submission.objects.filter(id=1)
    #output = ', '.join([sub.text for sub in submissions])
    #return HttpResponse(output)
    return render(request, "news.html")


def newest(request):
    return render(request, "newest.html")
