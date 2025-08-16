from django.db import models
from django.contrib.auth.models import AbstractUser

class School(models.Model):
    name = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    @property
    def location(self):
        if self.latitude and self.longitude:
            return (float(self.latitude), float(self.longitude))
        return None

class CustomUser(AbstractUser):
    national_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    ROLE_CHOICES = (
        ('system_admin', 'System Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student')
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, null=True, blank=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return str(self.username)

class Teacher(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    last_updated = models.DateTimeField(auto_now=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, default=1)
    bio = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    @property
    def location(self):
        if self.latitude and self.longitude:
            return (float(self.latitude), float(self.longitude))
        return None

    def __str__(self):
        return f"Teacher: {self.user.username}"

class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, default=1)
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    def __str__(self):
        return f"Student: {self.user.username}"