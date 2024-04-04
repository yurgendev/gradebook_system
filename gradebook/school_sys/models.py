from django.db import models
from users.models import Student, Teacher
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class SchoolClass(models.Model):
    class_name = models.CharField(max_length=2, unique=True, db_index=True)
    students = models.ManyToManyField(Student, related_name='classes')
    class_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='class_teacher')

    class Meta:
        ordering = ['students__last_name', 'students__first_name']

    def __str__(self):
        return self.class_name

    def remove_student(self, student):
        self.students.remove(student)


class Lesson(models.Model):
    SUBJECT_CHOICES = [
        ('math', 'Math'),
        ('it', 'IT'),
        ('english', 'English'),
        ('ukrainian', 'The Ukrainian Language'),
        ('deutch', 'Deutch'),
        ('geography', 'Geography'),
        ('art', 'Art'),
    ]

    lesson_date = models.DateField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, choices=SUBJECT_CHOICES)

    def __str__(self):
        return f"{self.get_subject_display()} - {self.lesson_date}"

    def clean(self):
        # Check that the teacher_id is not None
        if self.teacher_id is None:
            raise ValidationError('A lesson must have a teacher.')

        # Check that the lesson date is not in the past
        if self.lesson_date < timezone.now().date():
            raise ValidationError('The lesson date cannot be in the past.')

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)


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
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    grade_type = models.CharField(max_length=50, choices=GRADE_TYPES)

    def __str__(self):
        return str(self.value)



