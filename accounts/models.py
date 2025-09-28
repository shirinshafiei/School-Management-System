from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser, Group

class School(models.Model):
    name = models.CharField(max_length=20)
    location = models.PointField(geography=True, blank=True, null=True, srid=4326)


class CustomUser(AbstractUser):
    national_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.CharField(max_length=100, blank=True, null=True)
    location = models.PointField(geography=True, blank=True, null=True, srid=4326)

    USERNAME_FIELD = 'username'

    class Meta:
        permissions = [
            ("can_manage_system", "Can manage system settings"),
        ]


    def is_teacher(self):
        return self.groups.filter(name='teacher').exists()

    def is_student(self):
        return self.groups.filter(name='student').exists()

    def is_system_admin(self):
        return self.groups.filter(name='system_admin').exists() or self.is_superuser

    def __str__(self):
        return str(self.username)
