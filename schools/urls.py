from django.conf.urls.static import static
from django.urls import path

from config import settings
from .views import NewsCreateView, NewsUpdateView, ExerciseCreateView, ExerciseUpdateView, StudentEnrolledCoursesView, \
    StudentExerciseView, SubmissionCreateView, SubmissionUpdateView, NewsAdminViewSet, \
    ExerciseAdminViewSet, StudentNewsView, CourseCreateView, CourseListCreateAPIView, CourseRetrieveUpdateDestroyAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'admin/news', NewsAdminViewSet, basename='admin-news')
router.register(r'admin/exercises', ExerciseAdminViewSet, basename='admin-exercises')
# router.register(r'admin/courses', CourseAdminViewSet, basename='admin-courses')

urlpatterns = [
    path('create-news/', NewsCreateView.as_view(), name='news-create'),
    path('update-news/<int:pk>/', NewsUpdateView.as_view(), name='news-update'),

    path('create-exercises/', ExerciseCreateView.as_view(), name='exercise-create'),
    path('update-exercise/<int:pk>/', ExerciseUpdateView.as_view(), name='exercise-update'),

    path('student/course-view/', StudentEnrolledCoursesView.as_view(), name='student-enrolled-courses'),
    path('student/news-view/', StudentNewsView.as_view(), name='student-news-list'),
    path('student/exercise-view/', StudentExerciseView.as_view(), name='student-exercise-list'),

    path('student/create-submission/', SubmissionCreateView.as_view(), name='submission-create'),
    path('student/update-submission/<int:pk>/', SubmissionUpdateView.as_view(), name='submission-update'),

    path('create-course/', CourseCreateView.as_view(), name='course-create'),
    path('courses/', CourseListCreateAPIView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyAPIView.as_view(), name='course-detail'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += router.urls
