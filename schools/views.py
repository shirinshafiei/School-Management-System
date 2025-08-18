from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets, filters
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsSystemAdmin, IsStudent, IsTeacher
from .models import News, Exercise, Course, Submissions
from .serializers import CreateNewsSerializer, CreateExercisesSerializer, CourseSerializer, \
    ExerciseSerializer, NewsSerializer, CreateSubmissionsSerializer


class NewsCreateView(generics.CreateAPIView):
    serializer_class = CreateNewsSerializer
    permission_classes = [IsAuthenticated]


class NewsUpdateView(generics.UpdateAPIView):
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        user = self.request.user
        return News.objects.filter(course__teacher=user.teacher_profile)

class ExerciseCreateView(generics.CreateAPIView):
    serializer_class = CreateExercisesSerializer
    permission_classes = [IsAuthenticated]


class ExerciseUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateExercisesSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        user = self.request.user
        return Exercise.objects.filter(course__teacher=user.teacher_profile)



class StudentEnrolledCoursesView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(
            student=user.student_profile
        ).select_related('teacher').distinct()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['course', 'title']
    search_fields = ['title', 'body']


class StudentExerciseView(generics.ListAPIView):
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['course', 'title']
    search_fields = ['title', 'body']

    def get_queryset(self):
        user = self.request.user
        return Exercise.objects.filter(
            course__students=user.student_profile
        ).select_related('course').distinct()


class StudentNewsView(generics.ListAPIView):
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        user = self.request.user
        return News.objects.filter(
            course__student=user.student_profile
        ).select_related('course').distinct()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['course', 'title']
    search_fields = ['title', 'body']


class SubmissionCreateView(generics.CreateAPIView):
    serializer_class = CreateSubmissionsSerializer
    permission_classes = [IsAuthenticated]

class SubmissionUpdateView(generics.UpdateAPIView):
    serializer_class = CreateSubmissionsSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        user = self.request.user
        return Submissions.objects.filter(student=user.student_profile)

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