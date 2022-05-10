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
    if request.method == 'GET':
        submission = Submission.objects.get(id=submission_id)
        return JsonResponse(model_to_dict(submission), safe=False)
    else if request.method == 'POST':
        comment = Comment(author=request.user, submission=submission, text=request.POST['text'])
        comment.save()
        return JsonResponse(model_to_dict(comment), safe=False)

