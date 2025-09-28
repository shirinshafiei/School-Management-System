from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from schools.models import Course
User = get_user_model()

from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import CustomUser as User, School


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id", "username", "first_name",
            "last_name", "national_id", "is_active"
        )


class SchoolSerializer(serializers.ModelSerializer):
    location = serializers.ListField(
        child=serializers.FloatField(),
        write_only=True,
    )

    class Meta:
        model = School
        fields = ("id", "name", "location")

    def create(self, validated_data):
        lat, lng = validated_data.pop("location")
        validated_data["location"] = Point(lng, lat, srid=4326)
        return super().create(validated_data)

class TeacherSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "first_name",
                  "last_name", "email", "national_id")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            national_id=validated_data["national_id"],
            is_active=False
        )
        teacher_group = Group.objects.get(name='teacher')
        user.groups.add(teacher_group)
        return user


class StudentSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password",
                  "first_name", "last_name", "national_id")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            national_id=validated_data["national_id"],
            is_active=False
        )
        student_group = Group.objects.get(name='student')
        user.groups.add(student_group)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        return token


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    location = serializers.ListField(
        child=serializers.FloatField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "bio", "location"]

    def update(self, instance, validated_data):
        location = validated_data.pop("location", None)
        if location:
            lat, lng = location
            instance.location = Point(lng, lat, srid=4326)
        return super().update(instance, validated_data)


class AddStudentSerializer(serializers.Serializer):
    national_id = serializers.CharField(max_length=10)
    course_id = serializers.IntegerField()

    def validate_course_id(self, value):
        try:
            return Course.objects.get(id=value)
        except Course.DoesNotExist:
            raise serializers.ValidationError("Course does not exist")

    def validate_national_id(self, value):
        try:
            return User.objects.get(national_id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this national ID does not exist")

    def validate(self, data):
        course = data['course_id']
        student_user = data['national_id']

        student_group, _ = Group.objects.get_or_create(name="student")
        if not student_user.groups.filter(name="student").exists():
            student_user.groups.add(student_group)

        data['course'] = course
        data['student'] = student_user
        return data