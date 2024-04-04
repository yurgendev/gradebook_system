from django.test import TestCase
from school_sys.models import SchoolClass
from users.models import Student


class SchoolClassModelTest(TestCase):
    def setUp(self):
        self.student1 = Student.objects.create(
            first_name='Mark',
            last_name='Obi-Wan Kenobi',
            email='Mark.asd@google.com',
            date_of_birth='2005-01-01'
        )
        self.student2 = Student.objects.create(
            first_name='Orion',
            last_name='Wells',
            email='zzz.w123@example.com',
            date_of_birth='2005-02-01'
        )
        self.school_class = SchoolClass.objects.create(class_name='A')
        self.school_class.students.add(self.student1, self.student2)

    def test_school_class_creation(self):
        self.assertIsInstance(self.school_class, SchoolClass)
        self.assertEqual(self.school_class.__str__(), 'A')

    def test_remove_student(self):
        self.school_class.remove_student(self.student1)
        self.assertNotIn(self.student1, self.school_class.students.all())
        self.assertIn(self.student2, self.school_class.students.all())



from django.test import TestCase
from django.core.exceptions import ValidationError
from school_sys.models import Lesson, SchoolClass
from users.models import Teacher, Student
from datetime import datetime, timedelta

class LessonModelTest(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            date_of_birth='1980-01-01'
        )

    def test_lesson_without_teacher(self):
        with self.assertRaises(ValidationError):
            Lesson.objects.create(
                lesson_date='2023-03-01',
                subject='math'
            )

    def test_lesson_in_past(self):
        with self.assertRaises(ValidationError):
            Lesson.objects.create(
                lesson_date=(datetime.now() - timedelta(days=1)).date(),
                teacher=self.teacher,
                subject='math'
            )