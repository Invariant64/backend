import enum

from django.http import JsonResponse
from .models import Submission, Problem
from .execute import execute_all


def create_submission(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        problem_id = request.POST.get("problem_id")
        language = request.POST.get("language")
        code = request.POST.get("code")
        status = Submission.Status.PENDING
        submission = Submission(user_id=user_id, problem_id=problem_id, language=language, code=code, status=status)
        submission.save()

        problem = Problem.objects.get(id=problem_id)
        results = execute_all(problem, submission)
        for result in results:
            result.save()
        return JsonResponse({"status": "ok", "submission_id": submission.id})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"})


def get_submission(request, submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
        return JsonResponse({
            "status": "ok",
            "submission": {
                "id": submission.id,
                "user_id": submission.user_id,
                "problem_id": submission.problem_id,
                "language": submission.language,
                "code": submission.code,
                "result_id": submission.result_id,
                "status": submission.status,
                "time": submission.time
            }
        })
    except Submission.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Submission not found"})