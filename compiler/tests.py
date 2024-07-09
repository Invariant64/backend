from django.test import TestCase

from .models import Submission, Problem, TestCase as Test, Result
from .execute import execute_once, execute_all


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
            test_case_id=1,
            result="Accepted",
            execution_time=0.5,
            memory_used=64,
        )
        self.assertEqual(str(result), f"Result {result.id} for submission {result.submission_id}")


class ExecuteSimpleTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.languages = ["Python", "Java", "C++", "C"]
        self.problem = Problem.objects.create(
            title="Hello, World!",
            description="Write a program that prints 'Hello, World!' to the console.",
            input_description="There is no input for this problem.",
            output_description="Print 'Hello, World!' to the console.",
            sample_input="",
            sample_output="Hello, World!",
            time_limit=1,
            memory_limit=256,
        )
        self.test_cases = [
            Test.objects.create(
                problem_id=1,
                input="",
                output="Hello, World!",
                check_order=1,
            ),
            Test.objects.create(
                problem_id=1,
                input="5\n",
                output="Hello, World!",
                check_order=2,
            ),
            Test.objects.create(
                problem_id=1,
                input="11111",
                output="Hello, World!",
                check_order=3,
            ),
        ]

        self.codes = {
            "Python": {
                "Accepted": "print('Hello, World!')",
                "Wrong Answer": "print('123')",
                "Runtime Error": "1/0",
                "Time Limit Exceeded": "while True: pass",
            },
            "Java": {
                "Accepted": "public class Main {\n"
                            "    public static void main(String[] args) {\n"
                            "        System.out.println(\"Hello, World!\");\n"
                            "    }\n"
                            "}",
                "Wrong Answer": "public class Main {\n"
                                "    public static void main(String[] args) {\n"
                                "        System.out.println(\"123\");\n"
                                "    }\n"
                                "}",
                "Runtime Error": "public class Main {\n"
                                 "    public static void main(String[] args) {\n"
                                 "        System.out.println(1 / 0);\n"
                                 "    }\n"
                                 "}",
                "Time Limit Exceeded": "public class Main {\n"
                                       "    public static void main(String[] args) {\n"
                                       "        while (true) {}\n"
                                       "    }\n"
                                       "}",
            },
            "C++": {
                "Accepted": "#include <iostream>\n\n"
                            "int main() {\n"
                            "    std::cout << \"Hello, World!\" << std::endl;\n"
                            "    return 0;\n"
                            "}",
                "Wrong Answer": "#include <iostream>\n\n"
                                "int main() {\n"
                                "    std::cout << \"123\" << std::endl;\n"
                                "    return 0;\n"
                                "}",
                "Runtime Error": "#include <iostream>\n\n"
                                 "int main() {\n"
                                 "    int* p = nullptr;\n"
                                 "    *p = 1;\n"
                                 "    return 0;\n"
                                 "}",
                "Time Limit Exceeded": "#include <iostream>\n\n"
                                       "int main() {\n"
                                       "    while (true) {}\n"
                                       "    return 0;\n"
                                       "}",
            },
            "C": {
                "Accepted": "#include <stdio.h>\n\n"
                            "int main() {\n"
                            "    printf(\"Hello, World!\\n\");\n"
                            "    return 0;\n"
                            "}",
                "Wrong Answer": "#include <stdio.h>\n\n"
                                "int main() {\n"
                                "    printf(\"123\\n\");\n"
                                "    return 0;\n"
                                "}",
                "Runtime Error": "#include <stdio.h>\n\n"
                                 "int main() {\n    "
                                 "    void (*f)() = NULL;\n"
                                 "    f();\n"
                                 "    return 0;\n"
                                 "}",
                "Time Limit Exceeded": "#include <stdio.h>\n\n"
                                       "int main() {\n    "
                                       "while (1) {}\n"
                                       "    return 0;\n"
                                       "}",
            }
        }

    status = ["Accepted", "Wrong Answer", "Runtime Error", "Time Limit Exceeded"]

    def test_execute_once(self):
        for language in self.languages:
            for s in self.status:
                submission = Submission.objects.create(
                    user_id=1,
                    problem_id=1,
                    language=language,
                    code=self.codes[language][s],
                )
                for test_case in self.test_cases:
                    with self.subTest(language=language, status=s, test_case=test_case.id):
                        result = execute_once(self.problem, submission, test_case)
                        self.assertEqual(result.result, s, f"Language: {language}, Status: {s}, Test Case: {test_case.id}")

    def test_execute_all(self):
        for language in self.languages:
            for s in self.status:
                submission = Submission.objects.create(
                    user_id=1,
                    problem_id=1,
                    language=language,
                    code=self.codes[language][s],
                )
                with self.subTest(language=language, status=s):
                    results = execute_all(self.problem, submission)
                    for test_case, result in zip(self.test_cases, results):
                        self.assertEqual(result.result, s, f"Language: {language}, Status: {s}, Test Case: {test_case.id}")
