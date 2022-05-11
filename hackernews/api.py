from django.http import JsonResponse
from django.forms.models import model_to_dict
from hackernews.models import Submission, User, Comment, Action


def newsUser(request, username):
    if not User.objects.filter(authUser__username=username).exists():
        return JsonResponse({
            "status": 404,
            "error": "Not Found",
            "message": "No User with that username"
        }, status=404)
    submissions = list(Submission.objects.filter(author__authUser__username=username).values())
    return JsonResponse(submissions, safe=False)

def user(request, username):
    u = User.objects.get(authUser__username=username);
    return JsonResponse(model_to_dict(u), safe=False)

def detailedSubmission(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    return JsonResponse(model_to_dict(submission), safe=False)
