from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def submit(request):
    return render(request, "submit.html")


def news(request):
    return render(request, "news.html")


def newest(request):
    return render(request, "newest.html")
