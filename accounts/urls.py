from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import TeacherSignUpView, StudentSignUpView, CustomTokenObtainPairView, \
    AddStudentToCourseView, SchoolCreateView, \
    UserListView, UserApprovalView, LogoutView, ProfileUpdateView, NearestSchoolsListAPIView

urlpatterns = [
    path("signup/teacher/", TeacherSignUpView.as_view(), name="teacher-signup"),
    path("signup/student/", StudentSignUpView.as_view(), name="student-signup"),
    path('login/',CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='token_logout'),
    path('teacher/setup/', ProfileUpdateView.as_view(), name='teacher-profile-update'),
    path('add-student/', AddStudentToCourseView.as_view(), name='add-student'),
    path('teacher/update_profile/', ProfileUpdateView.as_view(), name='update-profile'),
    path('student/update-profile/', ProfileUpdateView.as_view(), name='update-profile'),
    path("schools/create/", SchoolCreateView.as_view(), name="school-create"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:user_id>/approval/", UserApprovalView.as_view(), name="user-approval"),
    path('nearest-schools/', NearestSchoolsListAPIView.as_view(), name='nearest-schools'),
]

