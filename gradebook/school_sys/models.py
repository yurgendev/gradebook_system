from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from schedule.models import Event
from schedule.models import Calendar


class SchoolClass(models.Model):
    class_name = models.CharField(max_length=2, unique=True, db_index=True)
    students = models.ManyToManyField('users.Student', related_name='classes')
    class_teacher = models.ForeignKey('users.Teacher', on_delete=models.SET_NULL, null=True,
                                      related_name='class_teacher')

    class Meta:
        ordering = ['students__last_name', 'students__first_name']

    def __str__(self):
        return self.class_name

    def remove_student(self, student):
        self.students.remove(student)


class Lesson(Event):
    SUBJECT_CHOICES = [
        ('math', 'Math'),
        ('it', 'IT'),
        ('english', 'English'),
        ('ukrainian', 'The Ukrainian Language'),
        ('deutch', 'Deutch'),
        ('geography', 'Geography'),
        ('art', 'Art'),
    ]
    LESSON_NUMBERS = [(i, str(i)) for i in range(1, 9)]

    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, choices=SUBJECT_CHOICES)
    lesson_number = models.IntegerField(choices=LESSON_NUMBERS, default=1)
    class_room = models.CharField(default='101', max_length=10)

    def __str__(self):
        return f"{self.get_subject_display()} - {self.start.date()}"

    def save(self, *args, **kwargs):
        self.start = self.start.replace(hour=0, minute=0, second=0)
        self.end = self.start

        super().save(*args, **kwargs)


class Grade(models.Model):
    GRADE_TYPES = [
        ('homework', 'Homework'),
        ('lesson', 'Lesson'),
        ('independent_work', 'Independent work'),
        ('test', 'Test'),
        ('control_work', 'Control work'),
        ('final', 'Final'),
    ]

    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    grade_type = models.CharField(max_length=50, choices=GRADE_TYPES)

    def __str__(self):
        return str(self.value)
