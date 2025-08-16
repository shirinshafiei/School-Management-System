from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from schools.models import Enrollment
from .permissions import IsProfileOwner, IsSystemAdmin
from .serializers import TeacherSignUpSerializer, StudentSignUpSerializer, CustomTokenObtainPairSerializer, \
    TeacherProfileSetSerializer, AddStudentSerializer, TeacherProfileUpdate, StudentProfileUpdate, UserSerializer, \
    SchoolSerializer
from .models import Teacher, Student, School
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
User = get_user_model()

class TeacherSignUpView(CreateAPIView):
    serializer_class = TeacherSignUpSerializer
    permission_classes = [AllowAny]

class StudentSignUpView(CreateAPIView):
    serializer_class = StudentSignUpSerializer
    permission_classes = [AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class TeacherProfileSetUpView(generics.RetrieveUpdateAPIView):
    serializer_class = TeacherProfileSetSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_object(self):
        if not hasattr(self.request.user, 'teacher_profile'):
            raise PermissionDenied("Only teachers can access this view.")
        return self.request.user.teacher_profile

class AddStudentToCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddStudentSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            student = serializer.validated_data['student']
            course = serializer.validated_data['course']

            Enrollment.objects.create(
                course=course,
                student=student
            )

            return Response({"detail": "student added successfully"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeacherProfileUpdateView(generics.UpdateAPIView):
    serializer_class = TeacherProfileUpdate
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_object(self):
        if not hasattr(self.request.user, 'teacher_profile'):
            raise PermissionDenied("Only teachers can access this view.")
        return self.request.user.teacher_profile


class StudentProfileUpdateView(generics.UpdateAPIView):
    serializer_class = StudentProfileUpdate
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_object(self):
        if not hasattr(self.request.user, 'student_profile'):
            raise PermissionDenied("Only students can access this view.")
        return self.request.user.student_profile

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSystemAdmin]

    def get_queryset(self):
        role = self.request.query_params.get('role')
        if role in ['teacher', 'student']:
            return User.objects.filter(role=role)
        return User.objects.all()


class UserApprovalView(APIView):
    permission_classes = [IsAuthenticated, IsSystemAdmin]

    def post(self, request, user_id):
        action = request.data.get("action")
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=404)

        if action == "approve":
            user.is_active = True
        elif action == "reject":
            user.is_active = False
        else:
            return Response({"detail": "Invalid action"}, status=400)

        user.save()
        return Response({"detail": f"User {action}d successfully"})

class SchoolCreateView(generics.CreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated, IsSystemAdmin]

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"error": "Token is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)
