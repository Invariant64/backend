from django.db import models


class Submission(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 0
        RUNNING = 1
        COMPLETED = 2
        FAILED = 3

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    problem_id = models.IntegerField()
    language = models.CharField(max_length=100)
    code = models.TextField()
    result_id = models.IntegerField(null=True)
    status = models.IntegerField(default=Status.PENDING)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission {self.id} by {self.user_id} on {self.time}"

    class Meta:
        db_table = "submissions"
        ordering = ["-time"]


class Problem(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    input_description = models.TextField()
    output_description = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    time_limit = models.IntegerField()
    memory_limit = models.IntegerField()

    def __str__(self):
        return f"Problem {self.id}: {self.title}"

    class Meta:
        db_table = "problems"
        ordering = ["id"]


class Result(models.Model):
    id = models.AutoField(primary_key=True)
    submission_id = models.IntegerField()
    result = models.CharField(max_length=100)
    execution_time = models.FloatField()
    memory_used = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result {self.id} for submission {self.submission_id}"

    class Meta:
        db_table = "results"
        ordering = ["-time"]


class TestCase(models.Model):
    id = models.AutoField(primary_key=True)
    problem_id = models.IntegerField()
    input = models.TextField()
    output = models.TextField()
    check_order = models.IntegerField()

    def __str__(self):
        return f"Test case {self.id} for problem {self.problem_id}"

    class Meta:
        db_table = "test_cases"
        ordering = ["id"]

