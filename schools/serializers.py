from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from django.utils import timezone

from .models import (
    Course, Enrollment, Exercise, News, Submissions
)
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "subject", "name", "teacher", "school")


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ("id", "course", "student")


class NewsSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.CharField(required=False)
    body = serializers.CharField(required=False)
    last_updated = serializers.DateTimeField(read_only=True)
    class Meta:
        model = News
        fields = ("id", "course", "title", "body", "last_updated")

class ExerciseSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.CharField(required=False)
    body = serializers.CharField(required=False)
    attached = serializers.FileField(required=False)
    last_updated = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Exercise
        fields = (
            "id", "course", "title", "body",
            "created_at", "deadline", "attached"
        )
        read_only_fields = ("created_at",)

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submissions
        fields = (
            "id", "exercise",
            "student", "answer", "created_at"
        )
        read_only_fields = ("created_at",)

class CreateNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'course', 'title', 'body', 'created_at', 'last_updated']
        read_only_fields = ['id', 'created_at', 'last_updated']

    def validate_course(self, value):
        user = self.context['request'].user
        if value.teacher != user.teacher_profile:
            raise serializers.ValidationError("You are not allowed to manage news for this course")
        return value

class CreateExercisesSerializer(serializers.ModelSerializer):
    attached = serializers.FileField(
        required=False,
        allow_null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'zip', 'txt'])
        ],
    )

    class Meta:
        model = Exercise
        fields = ['id', 'course', 'title', 'body', 'created_at', 'last_updated', 'deadline', 'attached']
        read_only_fields = ['id', 'created_at', 'last_updated']

    def validate_course(self, value):
        user = self.context['request'].user
        if value.teacher != user.teacher_profile:
            raise serializers.ValidationError("You are not allowed to manage news for this course")
        return value

class CreateSubmissionsSerializer(serializers.ModelSerializer):
    answer = serializers.FileField(
        required=False,
        allow_null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'zip', 'txt'])
        ],
    )

    class Meta:
        model = Submissions
        fields = ['id', 'exercise', 'student', 'created_at', 'answer']
        read_only_fields = ['id', 'created_at', 'student']

    def validate(self, data):

        request = self.context.get('request')
        exercise = data.get('exercise')
        student_profile = getattr(request.user, 'student_profile', None)

        data['student'] = student_profile

        if exercise.deadline and exercise.deadline < timezone.now():
            raise serializers.ValidationError(
                {"exercise": "The submission deadline has passed"}
            )

        return data

    def validate_exercise(self, exercise):
        request = self.context.get('request')
        student_profile = getattr(request.user, 'student_profile', None)

        is_enrolled = Enrollment.objects.filter(
            student=student_profile,
            course=exercise.course
        ).exists()

        if not is_enrolled:
            raise serializers.ValidationError(
                "You are not enrolled in this course and cannot submit answers"
            )

        return exercise
