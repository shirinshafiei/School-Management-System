from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import TeacherSignUpView, StudentSignUpView, CustomTokenObtainPairView, TeacherProfileSetUpView, \
    AddStudentToCourseView, TeacherProfileUpdateView, StudentProfileUpdateView, SchoolCreateView, \
    UserListView, UserApprovalView, LogoutView

urlpatterns = [
    path("signup/teacher/", TeacherSignUpView.as_view(), name="teacher-signup"),
    path("signup/student/", StudentSignUpView.as_view(), name="student-signup"),
    path('login/',CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='token_logout'),
    path('teacher/setup/', TeacherProfileSetUpView.as_view(), name='teacher-profile-update'),
    path('add-student/', AddStudentToCourseView.as_view(), name='add-student'),
    path('teacher/update_profile/', TeacherProfileUpdateView.as_view(), name='update-profile'),
    path('student/update-profile/', StudentProfileUpdateView.as_view(), name='update-profile'),
    path("schools/create/", SchoolCreateView.as_view(), name="school-create"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:user_id>/approval/", UserApprovalView.as_view(), name="user-approval"),
]

