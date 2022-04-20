from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.shortcuts import redirect

from hackernews.models import Submission, User, Comment, Action
from .forms import UserForm

def submit(request):
    return render(request, "submit.html")

def news(request):
    submissions_list = set(Submission.objects.order_by('-upvotes'))
    user = User.objects.get(id=1) #fake ought to be the logged user
    upvotes = Action.objects.filter(user=user, action_type=Action.UPVOTE_COMMENT)
    template = loader.get_template('news.html')
    context = {
        'submissions_list' : submissions_list,
        'upvotes' : upvotes,
        'title' : '',
        'user' : user
    }
    return HttpResponse(template.render(context, request))

def newsWelcome(request):
    return render(request, "newswelcome.html")

def newsUser(request, username):
    submissions_list = Submission.objects.filter(author__username=username)
    print("hola")
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

def upvote(request, submission_id):
#    if not request.user.is_authenticated():
#        return HttpResponse('user.html')
#    else :
        s = Submission.objects.get(id=submission_id)
        #s.points += 1, com fer amb upvotes??
        #s.save() ??? 
        #u = User.objects.get(username=request.user) #ARREGLAR! Treure?
        #u.id_submissions_upvotes.append(s.id)

        u = User.objects.get(id=1) #fake ought to be the logged user
        #u.id_submissions_upvotes.append(s.id)

        #Action.objects.create(content_object=submissionx, action_type=Action.UPVOTE_SUBMISSION, user=request.user)

        s.upvotes.create(action_type=Action.UPVOTE_SUBMISSION, user=u)

        #upvotes = Action.objects.filter(user=u, action_type=Action.UPVOTE_COMMENT)

        #s.upvotes += 1;

        #news(request)


        #submissions_list = Submission.objects.order_by('-upvotes')
        #template = loader.get_template('news.html') #Fer un redirect to /news?
        #context = {
        #    'submissions_list' : submissions_list,
        #    'user' : u,
        #}

        
        current_url = request.path
        
        if current_url[0:5] == '/news':
            return redirect('/news')

        elif current_url[0:7] == '/newest':
            return redirect('/newest')

        else: return redirect('/')
        

def comments(request, submission_id):
    s = Submission.objects.get(id=submission_id)
    c = Comment.objects.filter(submission=s)
    user = User.objects.get(id=1) #fake ought to be the logged user

    template = loader.get_template('comment.html')
    context = {
        'comments_list' : c,
        'user' : user
    }
    return HttpResponse(template.render(context, request))
