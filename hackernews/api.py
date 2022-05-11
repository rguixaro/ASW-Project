from django.http import JsonResponse
from django.forms.models import model_to_dict
from hackernews.models import Submission, User, Comment, Action
from datetime import date, datetime


def newsUser(request, username):
    if not User.objects.filter(authUser__username=username).exists():
        return JsonResponse({
            "status": 404,
            "error": "Not Found",
            "message": "No User with that username"
        }, status=404)
    submissions = list(Submission.objects.filter(author__authUser__username=username).values())
    return JsonResponse(submissions, safe=False)

def submission(request, title, url, text):
    if request.method == 'POST':
        author = User.objects.get(id=request.user.id)
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

        return JsonResponse(newSubmission, safe=False)

    elif request.method == 'GET':
        submissions = list(Submission.objects.values())
        return JsonResponse(submissions, safe=False)

def user(request, username):
    u = User.objects.get(authUser__username=username);
    return JsonResponse(model_to_dict(u), safe=False)

def detailedSubmission(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    return JsonResponse(model_to_dict(submission), safe=False)

def dateSubmissions(request, date):
    data = datetime.strptime(date, "%Y-%m-%d").date()
    submissions = list(Submission.objects.filter(posted_at_date=data).values())
    return JsonResponse(submissions, safe=False)