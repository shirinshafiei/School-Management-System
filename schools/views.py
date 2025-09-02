from django_filters.rest_framework import DjangoFilterBackend
from guardian.shortcuts import assign_perm
from rest_framework import generics, permissions, viewsets, filters
from rest_framework.permissions import IsAuthenticated

from accounts.filters import IsCourseTeacherFilterBackend
from accounts.permissions import IsSystemAdmin
from .filters import StudentEnrolledFilterBackend
from .models import News, Exercise, Course, Submissions
from .permissions import IsCourseTeacher, IsEnrolledStudent
from .serializers import ExerciseSerializer, CourseSerializer, \
    ExerciseSerializer, NewsSerializer, CreateSubmissionsSerializer


class NewsCreateView(generics.CreateAPIView):
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated, IsCourseTeacher]
    queryset = News.objects.all()


class NewsUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated, IsCourseTeacher]
    queryset = News.objects.all()

class ExerciseCreateView(generics.CreateAPIView):
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated, IsCourseTeacher]
    queryset = Exercise.objects.all()

class ExerciseUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated, IsCourseTeacher]
    queryset = Exercise.objects.all()

class StudentEnrolledCoursesView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()
    filter_backends = [
        StudentEnrolledFilterBackend,
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    filterset_fields = ["subject", "name"]
    search_fields = ["name"]


class StudentExerciseView(generics.ListAPIView):
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Exercise.objects.select_related("course").all()
    filter_backends = [
        StudentEnrolledFilterBackend,
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    filterset_fields = ["course", "title"]
    search_fields = ["title", "body"]


class StudentNewsView(generics.ListAPIView):
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]
    queryset = News.objects.select_related("course").all()
    filter_backends = [
        StudentEnrolledFilterBackend,
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    filterset_fields = ["course", "title"]
    search_fields = ["title", "body"]

class SubmissionCreateView(generics.CreateAPIView):
    serializer_class = CreateSubmissionsSerializer
    permission_classes = [IsAuthenticated, IsEnrolledStudent]
    queryset = Submissions.objects.all()


class SubmissionUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateSubmissionsSerializer
    permission_classes = [IsAuthenticated, IsEnrolledStudent]
    queryset = Submissions.objects.all()

class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsSystemAdmin]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['subject', 'teacher', 'school']
    search_fields = ['name', 'subject']

class CourseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsSystemAdmin]

class CourseCreateView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsSystemAdmin]

    def perform_create(self, serializer):
        course = serializer.save()

        if course.teacher:
            assign_perm("change_course", course.teacher, course)
            assign_perm("delete_course", course.teacher, course)


class ExerciseListAPIView(generics.ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated, IsSystemAdmin]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['course', 'title']
    search_fields = ['title', 'body']

class ExerciseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated, IsSystemAdmin]

class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated, IsSystemAdmin]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['course', 'title']
    search_fields = ['title', 'body']

class NewsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated, IsSystemAdmin]