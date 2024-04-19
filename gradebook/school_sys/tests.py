from django.test import TestCase
from django.utils import timezone
from schedule.models import Calendar
from .models import Lesson
from users.models import Teacher


class LessonModelTest(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(first_name="Test Teacher")
        self.calendar = Calendar.objects.create(name="Test Calendar")
        self.lesson = Lesson.objects.create(
            teacher=self.teacher,
            subject='math',
            start=timezone.now(),
            end=timezone.now(),
            calendar=self.calendar
        )

    def test_lesson_creation(self):
        self.assertEqual(self.lesson.teacher, self.teacher)
        self.assertEqual(self.lesson.subject, 'math')
        self.assertEqual(self.lesson.start.date(), timezone.now().date())
        self.assertEqual(self.lesson.end.date(), timezone.now().date())

    def test_str_representation(self):
        self.assertEqual(str(self.lesson), f"Math - {self.lesson.start.date()}")
