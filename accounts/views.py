from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from schools.models import  Course
from .filters import IsCourseTeacherFilterBackend
from .permissions import IsProfileOwner, IsSystemAdmin
from .serializers import TeacherSignUpSerializer, StudentSignUpSerializer, CustomTokenObtainPairSerializer, \
     AddStudentSerializer, UserSerializer, \
    SchoolSerializer, UserProfileUpdateSerializer
from .models import School
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

class AddStudentToCourseView(generics.GenericAPIView):
    serializer_class = AddStudentSerializer
    queryset = Course.objects.all()
    filter_backends = [IsCourseTeacherFilterBackend]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        student = serializer.validated_data['student']
        course = serializer.validated_data['course']

        course.students.add(student)

        return Response({"detail": "student added successfully"}, status=status.HTTP_200_OK)

class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_object(self):
        return self.request.user

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSystemAdmin]

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
    permission_classes = [IsAuthenticated]

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
