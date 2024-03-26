from django.db import models
from users.models import Student, Teacher
from django.core.validators import MinValueValidator, MaxValueValidator


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
