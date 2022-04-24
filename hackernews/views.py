from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db.models import Count

from hackernews.models import Submission, User, Comment, Action
from .forms import UserForm

@login_required(login_url='/login/')
def submitComment(request):
    if request.method == 'POST':
        text = request.POST['text']
        if text == "":
            return HttpResponse("Text no pot ser buit")
        id = request.POST['parent']
        s = Submission.objects.get(id=id)
        author = User.objects.get(id=request.user.id)
        newComment = Comment(text=text, author=author, submission=s)
        newComment.save()

@login_required(login_url='/login/')
def submitReply(request):
    if request.method == 'POST':
        text = request.POST['text']
        if text == "":
            return HttpResponse("Text no pot ser buit")
        id = request.POST['submission']
        s = Submission.objects.get(id=id)
        idc = request.POST['parent']
        p = Comment.objects.get(id=idc)
        author = User.objects.get(id=request.user.id)
        newComment = Comment(text=text, author=author, submission=s, parent=p)
        newComment.save()
        request.method = 'GET'
        return detailedSubmission(request, id)

@login_required(login_url='/login/')
def submit(request):
    if request.method == 'POST':
        title = request.POST['title']
        if title == "":
            return HttpResponse("Title no pot ser buit")
        url = request.POST['url']
        text = request.POST['text']
        author = User.objects.get(id=request.user.id)

        if url != "":
            if Submission.objects.filter(url=url).exists():
                id = Submission.objects.get(url=url).id
                return detailedSubmission(request, id)
            else:
                newSubmission = Submission(title=title, url=url, author=author)
                newSubmission.save()
                if text != "":
                    newComment = Comment(author=author, submission=newSubmission, text=text)
                    newComment.save()
        elif text != "":
            newSubmission = Submission(title=title, text=text, type="ask", author=author)
            newSubmission.save()
        else:
            return HttpResponse("URL i Text no pot ser buit")
        return HttpResponseRedirect('/news')

    return render(request, "submit.html")

def news(request):
    submissions_list = Submission.objects.annotate(count=Count('upvotes')).order_by('-count')
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        unvotesId = set(Submission.objects.values_list("id", flat=True)) - set(Action.objects.filter(user=user, action_type=Action.UPVOTE_SUBMISSION).values_list("id", flat=True))
    else:
        unvotesId = Action.objects.none()
    
    
    #print(unvotesId)
    template = loader.get_template('news.html')
    context = {
        'submissions_list' : submissions_list,
        'unvotesId' : unvotesId,
        'title' : '',
    }
    return HttpResponse(template.render(context, request))

def newsWelcome(request):
    return render(request, "newswelcome.html")

def newsUser(request, username):
    submissions_list = Submission.objects.filter(author__authUser__username=username)
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        upvotes = Action.objects.filter(user=user, action_type=Action.UPVOTE_SUBMISSION)
    else:
        upvotes = Action.objects.none()
    upvotesId = upvotes.values_list("id", flat=True)
    template = loader.get_template('news.html')
    context = {
        'submissions_list' : submissions_list,
        'title' : username+"'s submissions",
        'upvotesId' : upvotesId
    }
    return HttpResponse(template.render(context, request))

def newsDate(request, date):
    submissions_list = Submission.objects.filter(posted_at_date=date)
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        upvotes = Action.objects.filter(user=user, action_type=Action.UPVOTE_SUBMISSION)
    else:
        upvotes = Action.objects.none()
    upvotesId = upvotes.values_list("id", flat=True)
    template = loader.get_template('news.html')
    context = {
        'submissions_list' : submissions_list,
        'title' : date,
        'upvotesId' : upvotesId,
    }
    return HttpResponse(template.render(context, request))

def newest(request):
    submissions_list = Submission.objects.order_by('-posted_at_date', '-posted_at_time')
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        upvotes = Action.objects.filter(user=user, action_type=Action.UPVOTE_SUBMISSION)
    else:
        upvotes = Action.objects.none()
    upvotesId = upvotes.values_list("id", flat=True)
    template = loader.get_template('news.html')
    context = {
        'submissions_list': submissions_list,
        'title' : '',
        'upvotesId' : upvotesId,
    }
    return HttpResponse(template.render(context, request))

def user(request, username):
    u = User.objects.get(authUser__username=username)
    template = loader.get_template('user.html')
    if request.user.is_authenticated:
        print('logged-in')
    else:
        print('not logged-in')

    initialData = {'about': u.about,
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

@login_required(login_url='/login/')
def upvotedSubmissions(request, username):
    user = User.objects.get(authUser__username=username)
    upvotes = Action.objects.filter(user=user, action_type=Action.UPVOTE_SUBMISSION)
    template = loader.get_template('upvoted.html')
    return HttpResponse(template.render({'user' : user,'upvotes' : upvotes}, request))

@login_required(login_url='/login/')
def upvotedComments(request, username):
    user = User.objects.get(authUser__username=username)
    upvotes = Action.objects.filter(user=user, action_type=Action.UPVOTE_COMMENT)
    template = loader.get_template('upvoted.html')
    return HttpResponse(template.render({'user' : user,'upvotes' : upvotes}, request))

@login_required(login_url='/login/')
def threads(request, username):
    u = User.objects.get(authUser__username=username)
    comments_list = Comment.objects.filter(author = u)
    template = loader.get_template('threads.html')
    context = {
        'user' : u,
        'comments_list' : comments_list,
    }
    return HttpResponse(template.render(context, request))

def detailedSubmission(request, submission_id):
    if request.method == 'POST':
        submitComment(request)

    s = Submission.objects.get(id=submission_id)
    comments_list = Comment.objects.filter(submission=s)
    template = loader.get_template('submission.html')
    context = {
        'submission' : s,
        'comments_list' : comments_list,
    }

    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
def reply(request, comment_id):
    if request.method == 'POST':
        submitReply(request)

    u = User.objects.get(id=request.user.id)
    c = Comment.objects.get(id=comment_id)
    template = loader.get_template('reply.html')
    context = {
        'user' : u,
        'comment' : c,
    }
    return HttpResponse(template.render(context, request))

def ask(request):
    submissions_list = Submission.objects.filter(type="ask")
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        upvotes = Action.objects.filter(user=user, action_type=Action.UPVOTE_SUBMISSION)
    else:
        upvotes = Action.objects.none()
    upvotesId = upvotes.values_list("id", flat=True)
    template = loader.get_template('news.html')
    context = {
        'submissions_list': submissions_list,
        'upvotesId' : upvotesId,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
def upvote(request, submission_id):
    s = Submission.objects.get(id=submission_id)
    user = User.objects.get(id=request.user.id)

    if s.unvotes.filter(action_type=Action.UNVOTE_SUBMISSION, user=user).exists():
        s.unvotes.filter(action_type=Action.UNVOTE_SUBMISSION, user=user).delete()
    if not s.upvotes.filter(action_type=Action.UPVOTE_SUBMISSION, user=user).exists():
        s.upvotes.create(action_type=Action.UPVOTE_SUBMISSION, user=user)

    current_url = request.path

    if current_url[0:5] == '/news':
        return redirect('/news')

    elif current_url[0:7] == '/newest':
        return redirect('/newest')

    else: return redirect('/')


@login_required(login_url='/login/')
def unvote(request, submission_id):
    s = Submission.objects.get(id=submission_id)
    user = User.objects.get(id=request.user.id)

    if s.upvotes.filter(action_type=Action.UPVOTE_SUBMISSION, user=user).exists():
        s.upvotes.filter(action_type=Action.UPVOTE_SUBMISSION, user=user).delete()
    if not s.unvotes.filter(action_type=Action.UNVOTE_SUBMISSION, user=user).exists():
        s.unvotes.create(action_type=Action.UNVOTE_SUBMISSION, user=user)

    current_url = request.path

    if current_url[0:5] == '/news':
        return redirect('/news')

    elif current_url[0:7] == '/newest':
        return redirect('/newest')

    else: return redirect('/')


def comments(request, submission_id):
    s = Submission.objects.get(id=submission_id)
    c = Comment.objects.filter(submission=s)
    user = User.objects.get(id=request.user.id)

    template = loader.get_template('comment.html')
    context = {
        'comments_list' : c,
        'user' : user
    }
    return HttpResponse(template.render(context, request))


def login(request):
    #print("hola")
    return render(request, "login.html")

