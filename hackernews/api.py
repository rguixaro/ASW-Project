from django.http import JsonResponse
from django.forms.models import model_to_dict
from hackernews.models import Submission, User, Comment, Action


def newsUser(request, username):
    submissions = list(Submission.objects.filter(author__authUser__username=username).values())
    return JsonResponse(submissions, safe=False)

def user(request, username):
    u = User.objects.get(authUser__username=username);
    return JsonResponse(model_to_dict(u), safe=False)
    
def detailedSubmission(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    return JsonResponse(model_to_dict(submission), safe=False)

def commentsUser(request, username):
    comments = list(Comment.objects.filter(author__authUser__username=username).values())
    return JsonResponse(comments, safe=False)

def commentSubmission(request, submission_id):
    s = Submission.object.get(id=submission_id)
    comments = list(Comment.objects.get(submission=s).values())
    return JsonResponse(comments, safe=False)