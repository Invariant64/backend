from .models import Submission, Problem, TestCase, Result
import subprocess
import os
import time
import sys
import hashlib
import enum


def create_hash_dict(code):
    hash_name = hashlib.md5(code.encode() + str(time.time()).encode()).hexdigest()
    os.mkdir(f"temp/{hash_name}")
    return hash_name


def execute_all(problem, submission):
    results = []
    for test_case in TestCase.objects.filter(problem_id=problem.id):
        result = execute_once(problem, submission, test_case)
        results.append(result)
    return results


def execute_once(problem, submission, test_case):
    executer = {
        "Python": execute_python,
        "Java": execute_java,
        "C++": execute_cpp,
        "C": execute_c99,
    }

    hash_name = create_hash_dict(submission.code)
    result = Result(submission_id=submission.id, test_case_id=test_case.id)
    result = executer[submission.language](problem, submission, test_case, hash_name, result)
    os.rmdir(f"temp/{hash_name}")
    return result


def execute_python(problem, submission, test_case, hash_name, result):
    file_name = f"temp/{hash_name}/{hash_name}.py"
    with open(file_name, "w") as f:
        f.write(submission.code)
    try:
        start_time = time.time()
        execute_result = subprocess.run(
            args=[sys.executable, file_name],
            input=test_case.input,
            text=True,
            capture_output=True,
            timeout=problem.time_limit,
        )
        end_time = time.time()
        result.output = execute_result.stdout.strip()
        result.execution_time = end_time - start_time
        if execute_result.returncode != 0:
            result.result = "Runtime Error"
        elif result.output == test_case.output:
            result.result = "Accepted"
        else:
            result.result = "Wrong Answer"
    except subprocess.TimeoutExpired as e:
        result.result = "Time Limit Exceeded"

    result.memory_used = 0
    os.remove(file_name)
    return result


def execute_java(problem, submission, test_case, hash_name, result):
    class_name = "Main"
    code_file_name = f"temp/{hash_name}/{class_name}.java"
    class_file_name = f"temp/{hash_name}/{class_name}.class"
    with open(code_file_name, "w") as f:
        f.write(submission.code)
    try:
        compile_result = subprocess.run(
            args=["javac", "-d", f"temp/{hash_name}", code_file_name],
            text=True,
            capture_output=False,
            timeout=5,  # 5 seconds for compilation
        )
        if compile_result.returncode != 0:
            result.result = "Compilation Error"
            return result
        start_time = time.time()
        execute_result = subprocess.run(
            args=["java", "-cp", f"temp/{hash_name}", class_name],
            input=test_case.input,
            text=True,
            capture_output=True,
            timeout=problem.time_limit
        )
        end_time = time.time()
        result.output = execute_result.stdout.strip()
        result.execution_time = end_time - start_time
        if execute_result.returncode != 0:
            result.result = "Runtime Error"
        elif result.output == test_case.output:
            result.result = "Accepted"
        else:
            result.result = "Wrong Answer"
    except subprocess.TimeoutExpired as e:
        result.result = "Time Limit Exceeded"
    result.memory_used = 0
    os.remove(code_file_name)
    os.remove(class_file_name)
    return result


def execute_c(problem, submission, test_case, hash_name, result, mode="cpp"):
    code_file_name = f"temp/{hash_name}/{hash_name}." + mode
    exe_file_name = f"temp/{hash_name}/{hash_name}.exe"
    compiler = "g++" if mode == "cpp" else "gcc"
    with open(code_file_name, "w") as f:
        f.write(submission.code)
    try:
        compile_result = subprocess.run(
            args=[compiler, code_file_name, "-o", exe_file_name],
            text=True,
            capture_output=False,
            timeout=5,  # 5 seconds for compilation
        )
        if compile_result.returncode != 0:
            result.result = "Compilation Error"
            return result
        start_time = time.time()
        execute_result = subprocess.run(
            args=[exe_file_name],
            input=test_case.input,
            text=True,
            capture_output=True,
            timeout=problem.time_limit,
        )
        end_time = time.time()
        result.output = execute_result.stdout.strip()
        result.execution_time = end_time - start_time
        if execute_result.returncode != 0:
            result.result = "Runtime Error"
        elif result.output == test_case.output:
            result.result = "Accepted"
        else:
            result.result = "Wrong Answer"
    except subprocess.CalledProcessError as e:
        result.result = "Runtime Error"
    except subprocess.TimeoutExpired as e:
        result.result = "Time Limit Exceeded"
    result.memory_used = 0
    os.remove(code_file_name)
    os.remove(exe_file_name)
    return result


def execute_cpp(problem, submission, test_case, hash_name, result):
    return execute_c(problem, submission, test_case, hash_name, result, mode="cpp")


def execute_c99(problem, submission, test_case, hash_name, result):
    return execute_c(problem, submission, test_case, hash_name, result, mode="c")

