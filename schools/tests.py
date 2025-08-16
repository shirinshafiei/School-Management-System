from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from schools.models import Enrollment, Course, News, Exercise, Submissions
from accounts.models import Teacher, Student, School
from django.contrib.auth import get_user_model

User = get_user_model()

class SchoolApiTest(APITestCase):
    def test_teacher_can_create_news(self):
        school = School.objects.create(name="Test School")
        teacher_user = User.objects.create_user(username='teacher', password='pass', role='teacher')
        teacher = Teacher.objects.create(user=teacher_user, school=school)
        course = Course.objects.create(name="Math", teacher=teacher, school=school)

        self.client.force_authenticate(user=teacher_user)

        url = reverse('news-create')

        data = {
            "title": "New Chapter",
            "body": "Details about the new chapter...",
            "course": course.id
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_student_can_view_enrolled_courses(self):
        school = School.objects.create(name="Test School")
        student_user = User.objects.create_user(username='student', password='pass', role='student', national_id='1234555')
        student = Student.objects.create(user=student_user, school=school)

        teacher_user = User.objects.create_user(username='teacher', password='pass', role='teacher', national_id='1233333')
        teacher = Teacher.objects.create(user=teacher_user, school=school)

        course1 = Course.objects.create(name="Math", teacher=teacher, school=school)
        course2 = Course.objects.create(name="Science", teacher=teacher, school=school)

        Enrollment.objects.create(student=student, course=course1)

        self.client.force_authenticate(user=student_user)

        url = reverse('student-enrolled-courses')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], course1.id)

    # def test_student_can_create_submission(self):
    #     school = School.objects.create(name="Test School")
    #     student_user = User.objects.create_user(username='student', password='pass', role='student', national_id='1111111')
    #     student = Student.objects.create(user=student_user, school=school)
    #
    #     teacher_user = User.objects.create_user(username='teacher', password='pass', role='teacher', national_id='2222222')
    #     teacher = Teacher.objects.create(user=teacher_user, school=school)
    #
    #     course = Course.objects.create(name="Biology", teacher=teacher, school=school)
    #     Enrollment.objects.create(student=student, course=course)
    #
    #     exercise = Exercise.objects.create(title="Assignment 1", course=course)
    #
    #     self.client.force_authenticate(user=student_user)
    #
    #     url = reverse('submission-create')
    #
    #     data = {
    #         "exercise": exercise.id,
    #         "student": student.id,
    #         "answer": "My answer"
    #     }
    #
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(Submissions.objects.count(), 1)
