from ast import Sub
import json
from django.db.models import Count
from django.http import JsonResponse
from django.forms.models import model_to_dict
from hackernews.models import Submission, User, Comment, Action
from datetime import date, datetime, timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token


def getUserByToken(token):
    return Token.objects.get(key=token).user

def newsUser(request, username):
    if not User.objects.filter(authUser__username=username).exists():
        return JsonResponse({
            "status": 404,
            "error": "Not Found",
            "message": "No User with that username"
        }, status=404)
    submissions = list(Submission.objects.filter(author__authUser__username=username).values())
    return JsonResponse(submissions, safe=False)

@csrf_exempt
def submit(request):
    token = request.GET.get('token')
    username = getUserByToken(token).username
    author = User.objects.get(authUser__username=username)
    title = request.GET.get('title')
    url = request.GET.get('url')
    text = request.GET.get('text')
    if url != "":
        if Submission.objects.filter(url=url).exists():
            return JsonResponse({
                "status": 400,
                "error": "Bad Request",
                "message": "A submission with the same url was already posted"
            }, status=404)
        else:
            newSubmission = Submission(title=title, url=url, author=author)
            newSubmission.save()
            if text != "":
                newComment = Comment(author=author, submission=newSubmission, text=text)
                newComment.save()
    elif text != "":
        newSubmission = Submission(title=title, text=text, type="ask", author=author)
        newSubmission.save()

    return JsonResponse(model_to_dict(newSubmission), safe=False)

def news(request):
    submissions = list(Submission.objects.values().annotate(count=Count('upvotes')).order_by('-count'))
    for s in submissions:
        u = User.objects.get(id=s['author_id']);
        s['authorUsername'] = u.authUser.username
    return JsonResponse(submissions, safe=False)

def newest(request):
    submissions = list(Submission.objects.values().order_by('-posted_at_date', '-posted_at_time'))
    return JsonResponse(submissions, safe=False)

def ask(request):
    submissions = list(Submission.objects.values().filter(type="ask"))
    return JsonResponse(submissions, safe=False)

def user(request, username):
    u = User.objects.get(authUser__username=username)
    tmp1 = model_to_dict(u);
    tmp2 = model_to_dict(u.authUser)
    tmp1['username'] = tmp2['username'];
    tmp1['email'] = tmp2['email'];
    tmp1['age'] = u.age()
    return JsonResponse(tmp1, safe=False)

def detailedSubmission(request, submission_id, ):
    submission = Submission.objects.get(id=submission_id)
    s = model_to_dict(submission)
    s['upvotes'] = submission.upvotes.count()
    s['age'] = submission.age()
    s['authorUsername'] = submission.author.authUser.username
    return JsonResponse(s, safe=False)

def dateSubmissions(request, date):
    data = datetime.strptime(date, "%Y-%m-%d").date()
    submissions = list(Submission.objects.filter(posted_at_date=data).values())
    return JsonResponse(submissions, safe=False)

@csrf_exempt
def upvoteSubmission(request, submission_id):
    token = request.GET.get('token')
    username = getUserByToken(token).username
    user = User.objects.get(authUser__username=username)
    s = Submission.objects.get(id=submission_id)
    if s is None:
        return JsonResponse({
            "status": 404,
            "error": "Not Found",
            "message": "No Submission with that ID"
        }, status=404)
    if not s.upvotes.filter(action_type=Action.UPVOTE_SUBMISSION, user=user).exists():
        s.upvotes.create(action_type=Action.UPVOTE_SUBMISSION, user=user)
        return JsonResponse({"status": "success"}, safe=False)
    return JsonResponse({
        "status": 404,
        "error": "Already exists",
        "message": "Exists a user's upvote to this submission"
    }, status=404)

@csrf_exempt
def unvoteSubmission(request, submission_id):
    token = request.GET.get('token')
    username = getUserByToken(token).username
    user = User.objects.get(authUser__username=username)
    s = Submission.objects.get(id=submission_id)
    if s is None:
        return JsonResponse({
            "status": 404,
            "error": "Not Found",
            "message": "No Submission with that ID"
        }, status=404)
    if s.upvotes.filter(action_type=Action.UPVOTE_SUBMISSION, user=user).exists():
        s.upvotes.filter(action_type=Action.UPVOTE_SUBMISSION, user=user).delete()
        return JsonResponse({"status": "success"}, safe=False)
    return JsonResponse({
        "status": 404,
        "error": "Doesn't exists",
        "message": "Doesn't exists a user's upvote to this submission"
    }, status=404)

def upvotedSubmissions(request):
    token = request.GET.get('token')
    username = getUserByToken(token).username
    user = User.objects.get(authUser__username=username)
    upvoted = list(Action.objects.filter(user=user, action_type=Action.UPVOTE_SUBMISSION).values())
    return JsonResponse(upvoted, safe=False)

@csrf_exempt
def upvoteComment(request, comment_id):
    token = request.GET.get('token')
    username = getUserByToken(token).username
    user = User.objects.get(authUser__username=username)
    c = Comment.objects.get(id=comment_id)
    if c is None:
        return JsonResponse({
            "status": 404,
            "error": "Not Found",
            "message": "No Comment with that ID"
        }, status=404)
    if not c.upvotes.filter(action_type=Action.UPVOTE_COMMENT, user=user).exists():
        c.upvotes.create(action_type=Action.UPVOTE_COMMENT, user=user)
        return JsonResponse({"status": "success"}, safe=False)
    return JsonResponse({
        "status": 404,
        "error": "Already exists",
        "message": "Exists a user's upvote to this comment"
    }, status=404)

@csrf_exempt
def unvoteComment(request, comment_id):
    token = request.GET.get('token')
    username = getUserByToken(token).username
    user = User.objects.get(authUser__username=username)
    c = Comment.objects.get(id=comment_id)
    if c is None:
        return JsonResponse({
            "status": 404,
            "error": "Not Found",
            "message": "No Comment with that ID"
        }, status=404)
    if c.upvotes.filter(action_type=Action.UPVOTE_COMMENT, user=user).exists():
        c.upvotes.filter(action_type=Action.UPVOTE_COMMENT, user=user).delete()
        return JsonResponse({"status": "success"}, safe=False)
    return JsonResponse({
        "status": 404,
        "error": "Doesn't exists",
        "message": "Doesn't exists a user's upvote to this comment"
    }, status=404)

def upvotedComments(request):
    token = request.GET.get('token')
    username = getUserByToken(token).username
    user = User.objects.get(authUser__username=username)
    upvoted = list(Action.objects.filter(user=user, action_type=Action.UPVOTE_COMMENT).values())
    return JsonResponse(upvoted, safe=False)

def commentsUser(request, username):
    comments = list(Comment.objects.filter(author__authUser__username=username).values())
    return JsonResponse(comments, safe=False)

def commentsSubmission(request, submission_id):
    s = Submission.objects.get(id=submission_id)
    comments = list(Comment.objects.filter(submission=s).values())
    return JsonResponse(comments, safe=False)

@csrf_exempt
def commentSubmission(request, submission_id):
    text = request.GET.get('text')
    if text is None:
        return JsonResponse({
            "status": 400,
            "error": "No Text",
            "message": "Need text to comment"
        }, status=400)
    s = Submission.objects.get(id=submission_id)
    if s is None:
        return JsonResponse({
            "status": 404,
            "error": "Not Found",
            "message": "No Submission with that ID"
        }, status=404)
    token = request.GET.get('token')
    username = getUserByToken(token).username
    author = User.objects.get(authUser__username=username)
    newComment = Comment(text=text, author=author, submission=s)
    newComment.save()
    return JsonResponse({"status": "success"}, safe=False)

@csrf_exempt
def replyComment(request, comment_id):
    text = request.GET.get('text')
    if text is None:
        return JsonResponse({
            "status": 400,
            "error": "No Text",
            "message": "Need text to comment"
        }, status=400)
    c = Comment.objects.get(id=comment_id)
    if c is None:
        return JsonResponse({
            "status": 404,
            "error": "Not Found",
            "message": "No Comment with that ID"
        }, status=404)
    token = request.GET.get('token')
    username = getUserByToken(token).username
    author = User.objects.get(authUser__username=username)
    submission_id = c.submission.id
    s = Submission.objects.get(id=submission_id)
    newComment = Comment(text=text, author=author, submission=s, parent=c)
    newComment.save()
    return JsonResponse({"status": "success"}, safe=False)

@csrf_exempt
def editProfile(request):
    about = request.GET.get('about')
    if about is None:
        return JsonResponse({
            "status": 400,
            "error": "No Text",
            "message": "Need text to update about"
        }, status=400)
    token = request.GET.get('token')
    username = getUserByToken(token).username
    user = User.objects.get(authUser__username=username)
    user.about = about
    user.save()
    return JsonResponse({"status": "success"}, safe=False)
