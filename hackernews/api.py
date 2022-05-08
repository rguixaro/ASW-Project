from django.http import JsonResponse
from django.forms.models import model_to_dict
from hackernews.models import Submission, User, Comment, Action


def newsUser(request, username):
    submissions = list(Submission.objects.filter(author__authUser__username=username).values())
    return JsonResponse(submissions, safe=False)

def user(request, username):
    u = User.objects.get(authUser__username=username);
    return JsonResponse(model_to_dict(u), safe=False)

def submission(request, title, url, text):
    if request.method == 'POST':
        if title == "":
            return JsonResponse("Title no pot ser buit")
        author = User.objects.get(id=request.user.id)

        if url != "":
            if Submission.objects.filter(url=url).exists():
                return JsonResponse("Ja existeix una submission amb la mateixa url")
            else:
                newSubmission = Submission(title=title, url=url, author=author)
                newSubmission.save()
                if text != "":
                    newComment = Comment(author=author, submission=newSubmission, text=text)
                    newComment.save()

            return JsonResponse(newSubmission, safe=False)

        elif text != "":
            newSubmission = Submission(title=title, text=text, type="ask", author=author)
            newSubmission.save()
            return JsonResponse(newSubmission, safe=False)

    elif request.method == 'GET':
    submissions = list(Submission.objects.values())
    return JsonResponse(submissions, safe=False)