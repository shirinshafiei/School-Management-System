from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.permissions import  IsSystemAdmin
from .models import News, Exercise, Course, Submissions
from .serializers import CreateNewsSerializer, CreateExercisesSerializer, CourseSerializer, \
    ExerciseSerializer, NewsSerializer, CreateSubmissionsSerializer


class NewsCreateView(generics.CreateAPIView):
    serializer_class = CreateNewsSerializer
    permission_classes = [IsAuthenticated]


class NewsUpdateView(generics.UpdateAPIView):
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'teacher_profile'):
            return News.objects.filter(course__teacher=user.teacher_profile)
        return News.objects.none()

class ExerciseCreateView(generics.CreateAPIView):
    serializer_class = CreateExercisesSerializer
    permission_classes = [IsAuthenticated]


class ExerciseUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateExercisesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'teacher_profile'):
            return Exercise.objects.filter(course__teacher=user.teacher_profile)
        return Exercise.objects.none()


class StudentEnrolledCoursesView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        student_profile = getattr(user, 'student_profile', None)
        if student_profile:
            return Course.objects.filter(
                enrollment__student=student_profile
            ).select_related('teacher').distinct()
        return Course.objects.none()


class StudentExerciseView(generics.ListAPIView):
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        student_profile = getattr(user, 'student_profile', None)
        if student_profile:
            return Exercise.objects.filter(
                course__enrollment__student=student_profile
            ).select_related('course').distinct()
        return Exercise.objects.none()


class StudentNewsView(generics.ListAPIView):
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        student_profile = getattr(user, 'student_profile', None)
        if student_profile:
            return News.objects.filter(
                course__enrollment__student=student_profile
            ).select_related('course').distinct()
        return News.objects.none()

class SubmissionCreateView(generics.CreateAPIView):
    serializer_class = CreateSubmissionsSerializer
    permission_classes = [IsAuthenticated]

class SubmissionUpdateView(generics.UpdateAPIView):
    serializer_class = CreateSubmissionsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'student_profile'):
            return Submissions.objects.filter(student=user.student_profile)
        return Submissions.objects.none()

class NewsAdminViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated, IsSystemAdmin]

class ExerciseAdminViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated, IsSystemAdmin]

class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsSystemAdmin]

class CourseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsSystemAdmin]

class CourseCreateView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsSystemAdmin]

