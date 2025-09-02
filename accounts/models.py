from django.db import models
from django.contrib.auth.models import AbstractUser, Group

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
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    USERNAME_FIELD = 'username'

    class Meta:
        permissions = [
            ("can_manage_system", "Can manage system settings"),
        ]

    @property
    def location(self):
        if self.latitude and self.longitude:
            return (float(self.latitude), float(self.longitude))
        return None

    def is_teacher(self):
        return self.groups.filter(name='teacher').exists()

    def is_student(self):
        return self.groups.filter(name='student').exists()

    def is_system_admin(self):
        return self.groups.filter(name='system_admin').exists() or self.is_superuser

    def __str__(self):
        return str(self.username)
