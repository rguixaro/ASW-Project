import json
from django.http import JsonResponse
from django.forms.models import model_to_dict
from hackernews.models import Submission, User, Comment, Action
from datetime import date, datetime
from django.views.decorators.csrf import csrf_exempt


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
def user(request, username):
    u = User.objects.get(authUser__username=username);
    if(request.method == 'GET'):
        print("get")
        return JsonResponse(model_to_dict(u), safe=False)
    else:
        updatedUser = request.body.decode('utf-8')
        body = json.loads(updatedUser)
        u.about = body['about'];
        u.showdead = body['showDead'];
        u.noprocrast = body['noprocrast']
        u.maxvisit = body['maxvisit']
        u.minaway = body['minaway']
        u.delay = body['delay']
        u.save()
        return JsonResponse(model_to_dict(u), safe=False)


def detailedSubmission(request, submission_id):
    if request.method == 'GET':
        submission = Submission.objects.get(id=submission_id)
        s = model_to_dict(submission)
        s['upvotes'] = submission.upvotes.count()
        return JsonResponse(s, safe=False)
    else:
        if request.method == 'POST':
            text = request.POST['text']
            if text == "":
                return JsonResponse({'error': 'Empty comment'}, status=400)
            id = request.POST['parent']
            s = Submission.objects.get(id=id)
            author = User.objects.get(id=request.user.id)
            newComment = Comment(text=text, author=author, submission=s)
            newComment.save()
            return JsonResponse(model_to_dict(newComment), safe=False)

def dateSubmissions(request, date):
    data = datetime.strptime(date, "%Y-%m-%d").date()
    submissions = list(Submission.objects.filter(posted_at_date=data).values())
    return JsonResponse(submissions, safe=False)

def upvoteSubmission(request, submission_id):
    s = Submission.objects.get(id=submission_id)
    if not s.upvotes.filter(action_type=Action.UPVOTE_SUBMISSION, user=user).exists():
        s.upvotes.create(action_type=Action.UPVOTE_SUBMISSION, user=user)