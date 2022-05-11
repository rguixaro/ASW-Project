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


