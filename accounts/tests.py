from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from schools.models import Enrollment, Course
from accounts.models import Teacher, Student, School
from django.contrib.auth import get_user_model

User = get_user_model()

class UserApiTests(APITestCase):

    def test_teacher_signup(self):
        school = School.objects.create(
            id=1,
            name="school")
        url = reverse('teacher-signup')
        data = {
            'username': 'teacher1',
            'email': 'teacher1@example.com',
            'password': '1234',
            'first_name': 'shirin',
            'last_name': 'shafiei',
            'national_id': '1234567890'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='teacher1').exists())


    def test_add_student_to_course(self):
        school = School.objects.create(
            id=1,
            name="school")
        teacher_user = User.objects.create_user(username='teacher', password='pass', role='teacher')

        student_user = User.objects.create_user(username='student', password='pass', national_id='1234567890',
                                                    role='student')
        student = Student.objects.create(user=student_user, school= school)
        teacher = Teacher.objects.create(user=teacher_user, school=school)
        course = Course.objects.create(name="Test Course", teacher=teacher, school=school)
        self.client.force_authenticate(user=teacher_user)

        url = reverse('add-student')
        data = {
            'national_id': '1234567890',
            'course_id': course.id
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Enrollment.objects.filter(student=student, course=course).exists()
        )

        data2 = {
            'national_id': '9999999999',
            'course_id': course.id
        }

        response2 = self.client.post(url, data2)

        self.assertIn(response2.status_code, [400, 404])
        self.assertEqual(Enrollment.objects.count(), 1)

    def test_login(self):
        school = School.objects.create(
            id=1,
            name="school")

        User.objects.create_user(
            username='testuser',
            password='1234'
        )
        self.login_url = reverse('token_obtain_pair')

        data = {'username': 'testuser', 'password': '1234'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

        data2 = {'username': 'testuser', 'password': '123'}
        response = self.client.post(self.login_url, data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)