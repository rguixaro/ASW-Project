from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

from .forms import SubmitForm
from hackernews.models import Submission, User, Comment, Action
from .forms import UserForm

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


def news(request):
    submissions_list = set(Submission.objects.order_by('-upvotes'))
    user = User.objects.get(id=1) #fake ought to be the logged user
    template = loader.get_template('news.html')
    context = {
        'submissions_list' : submissions_list,
        'title' : '',
        'user' : user
    }
    return HttpResponse(template.render(context, request))

def newsWelcome(request):
    return render(request, "newswelcome.html")

def newsUser(request, username):
    submissions_list = Submission.objects.filter(author__username=username)
    user = User.objects.get(id=1) #fake ought to be the logged user
    template = loader.get_template('news.html')
    context = {
        'submissions_list' : submissions_list,
        'title' : username+"'s submissions",
        'user' : user
    }
    return HttpResponse(template.render(context, request))

def newsDate(request, date):
    submissions_list = Submission.objects.filter(posted_at_date=date)
    user = User.objects.get(id=1) #fake ought to be the logged user
    template = loader.get_template('news.html')
    context = {
        'submissions_list' : submissions_list,
        'title' : date,
        'user' : user
    }
    return HttpResponse(template.render(context, request))

def newest(request):
    submissions_list = Submission.objects.order_by('-posted_at_date', '-posted_at_time')
    user = User.objects.get(id=1) #fake ought to be the logged user
    template = loader.get_template('news.html')
    context = {
        'submissions_list': submissions_list,
        'title' : '',
        'user' : user
    }
    return HttpResponse(template.render(context, request))

def user(request, username):
    u = User.objects.get(username=username)
    template = loader.get_template('user.html')
    if request.user.is_authenticated:
        print('logged-in')
    else:
        print('not logged-in')

    initialData = {'about': u.about,
        'email': u.email,
        'showdead': u.showdead,
        'noprocrast': u.noprocrast,
        'maxvisit': u.maxvisit,
        'minaway': u.minaway,
        'delay': u.delay}

    #create user
        #userForm = UserForm(request.POST)
        #newUser = userForm.save()
    #update user
    if request.method == 'POST':
        userForm = UserForm(request.POST or None, instance=u)
        if userForm.is_valid():
            userForm.save()
    else:
        userForm = UserForm(initial=initialData)

    return HttpResponse(template.render({'user': u, 'form': userForm}, request))

def upvotedSubmissions(request, username):
    u = User.objects.get(username=username)
    upvotes = Action.objects.filter(user=u, action_type=Action.UPVOTE_SUBMISSION)
    template = loader.get_template('upvoted.html')
    return HttpResponse(template.render({'user' : u,'upvotes' : upvotes}, request))

def upvotedComments(request, username):
    u = User.objects.get(username=username)
    upvotes = Action.objects.filter(user=u, action_type=Action.UPVOTE_COMMENT)
    template = loader.get_template('upvoted.html')
    return HttpResponse(template.render({'user' : u,'upvotes' : upvotes}, request))

def threads(request, username):
    u = User.objects.get(username=username)
    comments_list = Comment.objects.filter(author = u)
    template = loader.get_template('threads.html')
    context = {
        'user' : u,
        'comments_list' : comments_list,
    }
    return HttpResponse(template.render(context, request))

def ask(request):
    submissions_list = Submission.objects.get(type="ask")
    template = loader.get_template('ask.html')
    context = {
        'submissions_list': submissions_list,
    }
    return HttpResponse(template.render(context, request))

