from django.core.validators import validate_email
from django.db import models
from django.db.models.functions import ExtractMonth, ExtractDay
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class PersonManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Person(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True, validators=[validate_email])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = PersonManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        components = [self.last_name, self.first_name, self.middle_name]
        formatted_str = ' '.join(component for component in components if component)
        return formatted_str.strip()


class Teacher(Person):
    # lessons = models.ManyToManyField(Lesson, related_name='teachers')

    class Meta:
        permissions = [
            ("add_news", "Can add news"),
            ("change_news", "Can change news"),
            ("delete_news", "Can delete news"),
            ("add_grade", "Can add grade"),
            ("change_grade", "Can change grade"),
            ("delete_grade", "Can delete grade"),
            ('add_diary_notes', 'Can add diary notes'),
        ]


class Parent(Person):
    children = models.ManyToManyField('Student')

    class Meta:
        permissions = [
            ("view_news", "Can view news"),
            ("view_grade", "Can view grade"),
        ]


class Student(Person):
    date_of_birth = models.DateField(null=True, blank=True)
    middle_name = None

    @classmethod
    def get_upcoming_birthdays(cls):
        today = datetime.today().date()
        thirty_days_later = today + timedelta(days=30)

        return cls.objects.annotate(
            month=ExtractMonth('date_of_birth'),
            day=ExtractDay('date_of_birth'),
        ).filter(
            month=today.month, day__gte=today.day
        ).union(
            cls.objects.annotate(
                month=ExtractMonth('date_of_birth'),
                day=ExtractDay('date_of_birth'),
            ).filter(
                month=thirty_days_later.month, day__lte=thirty_days_later.day
            )
        )

    class Meta:
        permissions = [
            ("view_news", "Can view news"),
            ("view_grade", "Can view grade"),
            ("add_diary_notes", "can add diary notes"),
        ]
