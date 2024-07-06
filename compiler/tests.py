from django.test import TestCase

from .models import Submission, Problem, TestCase as Test, Result


class SubmissionModelTest(TestCase):

    def test_string_representation(self):
        submission = Submission.objects.create(
            user_id=1,
            problem_id=1,
            language="Python",
            code="print('Hello, World!')",
        )
        self.assertEqual(str(submission), f"Submission {submission.id} by {submission.user_id} on {submission.time}")

    def test_default_status(self):
        submission = Submission.objects.create(
            user_id=1,
            problem_id=1,
            language="Python",
            code="print('Hello, World!')",
        )
        self.assertEqual(submission.status, Submission.Status.PENDING)


class ProblemModelTest(TestCase):

    def test_string_representation(self):
        problem = Problem.objects.create(
            title="Hello, World!",
            description="Write a program that prints 'Hello, World!' to the console.",
            input_description="There is no input for this problem.",
            output_description="Print 'Hello, World!' to the console.",
            sample_input="",
            sample_output="Hello, World!",
            time_limit=1,
            memory_limit=256,
        )
        self.assertEqual(str(problem), f"Problem {problem.id}: {problem.title}")


class TestCaseModelTest(TestCase):
    def test_string_representation(self):
        test_case = Test.objects.create(
            problem_id=1,
            input="5\n",
            output="5\n",
            check_order=1,
        )
        self.assertEqual(str(test_case), f"Test case {test_case.id} for problem {test_case.problem_id}")


class ResultModelTest(TestCase):
    def test_string_representation(self):
        result = Result.objects.create(
            submission_id=1,
            result="Accepted",
            execution_time=0.5,
            memory_used=64,
        )
        self.assertEqual(str(result), f"Result {result.id} for submission {result.submission_id}")

