from contextlib import nullcontext

from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import (
    School, Teacher, Student,
)
from schools.models import Course, Enrollment
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", "username", "email",
            "first_name", "last_name",
            "national_id", "role", "is_active"
        )

class SchoolSerializer(serializers.ModelSerializer):
    location = serializers.ListField(
        child=serializers.FloatField(),
        write_only=True,
        required=True,
        help_text="Latitude and Longitude as a list [lat, lng]"
    )

    class Meta:
        model = School
        fields = ("id", "name", "location")

    def create(self, validated_data):
        location = validated_data.pop('location')
        school = School.objects.create(
            name=validated_data['name'],
            latitude=location[0],
            longitude=location[1]
        )
        return school


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Teacher
        fields = ("id", "bio", "location")


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Student
        fields = ("id", "user", "school")


class TeacherSignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "password", "first_name",
                  "last_name", "email", "national_id")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            national_id=validated_data["national_id"],
            is_active=False,
            role="teacher"
        )
        Teacher.objects.create(user=user)
        return user


class StudentSignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "password",
                  "first_name", "last_name", "national_id")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            national_id=validated_data["national_id"],
            is_active=False,
            role="student"
        )
        Student.objects.create(user=user)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['role'] = user.role

        return token

class TeacherProfileSetSerializer(serializers.ModelSerializer):
    location = serializers.ListField(
        child=serializers.FloatField(),
        write_only=True,
        required=False,
        help_text="Latitude and Longitude as a list [lat, lng]"
    )

    class Meta:
        model = Teacher
        fields = ['bio', 'location']

    def update(self, instance, validated_data):
        bio = validated_data.get('bio')
        if bio is not None:
            instance.bio = bio

        location = validated_data.get('location')
        if location and len(location) == 2:
            instance.latitude = location[0]
            instance.longitude = location[1]

        instance.save()
        return instance

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        extra_kwargs = {
            'username': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

class TeacherProfileUpdate(serializers.ModelSerializer):
    user = UserUpdateSerializer()
    location = serializers.ListField(
        child=serializers.FloatField(),
        write_only=True,
        required=False,
        min_length=2,
        max_length=2
    )

    class Meta:
        model = Teacher
        fields = ['user', 'bio', 'location']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_serializer = UserUpdateSerializer(instance.user, data=user_data, partial=True)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()

        location = validated_data.pop('location', None)
        if location:
            instance.latitude, instance.longitude = location

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class StudentProfileUpdate(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = Student
        fields = ['user']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_serializer = UserUpdateSerializer(instance.user, data=user_data, partial=True)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class AddStudentSerializer(serializers.Serializer):
    national_id = serializers.CharField(max_length=10)
    course_id = serializers.IntegerField()

    def validate(self, data):
        national_id = data.get('national_id')
        course_id = data.get('course_id')

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError("Course does not Exist")

        request_user = self.context['request'].user
        if course.teacher.user != request_user:
            raise serializers.ValidationError("you can not acceess this course")


        try:
            student_user = User.objects.get(national_id=national_id, role='student')
        except User.DoesNotExist:
            raise serializers.ValidationError("student does not Exist")

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError("Course does not Exist")

        data['student'] = student_user.student_profile
        data['course'] = course
        return data

