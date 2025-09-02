from django.contrib.auth import get_user_model
from django.db import models
from accounts.models import School
User = get_user_model()


class Course(models.Model):
    subject = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="taught_courses"
    )
    students = models.ManyToManyField(
        User,
        related_name="enrolled_courses"
    )

class Exercise(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True)
    attached = models.FileField()

class News(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

class Submissions(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    answer = models.FileField()