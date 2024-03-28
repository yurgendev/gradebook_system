from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import Teacher, Parent, Student
from users.admin import TeacherAdmin, ParentAdmin, StudentAdmin
from django.contrib.admin.sites import AdminSite


class UsersModelsTest(TestCase):
    def test_teacher_str(self):
        teacher = Teacher.objects.create(
            first_name='Oksana',
            last_name='Yanchenko',
            middle_name='Yuriievna',
            email='op@ukraine.com'
        )

        self.assertEqual(
            str(teacher),
            'Yanchenko Oksana Yuriievna'
        )

    def test_parent_str(self):
        parent = Parent.objects.create(
            first_name='Anatolii',
            last_name='Ivanov',
            middle_name='',
            email='anatol@example.com'
        )
        self.assertEqual(str(parent), 'Ivanov Anatolii')

    def test_student_str(self):
        student = Student.objects.create(
            first_name='Vlad',
            last_name='Saloevskii',
            email='vlad@example.com'
        )
        self.assertEqual(str(student), 'Saloevskii Vlad')


class StudentModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            date_of_birth='2005-01-01'
        )
        self.parent = Parent.objects.create(
            first_name='Parent',
            last_name='Doe',
            email='parent.doe@example.com'
        )
        self.parent.children.add(self.student)

    def test_student_creation(self):
        self.assertEqual(self.student.first_name, 'John')
        self.assertEqual(self.student.last_name, 'Doe')
        self.assertEqual(self.student.email, 'john.doe@example.com')
        self.assertEqual(self.student.date_of_birth, '2005-01-01')

    def test_parent_children_relation(self):
        self.assertEqual(self.parent.children.first(), self.student)


# тесты


class UserModelTest(TestCase):
    # ...

    def test_email_validation(self):
        try:
            Teacher.objects.create_user(None)
        except ValueError as e:
            self.assertEqual(str(e), 'The Email field must be set')

    def test_upcoming_birthdays(self):
        student1 = Student.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            date_of_birth='2005-01-01'
        )
        student2 = Student.objects.create(
            first_name='Jane',
            last_name='Doe',
            email='jane.doe@example.com',
            date_of_birth='2005-02-01'
        )
        upcoming_birthdays = list(Student.get_upcoming_birthdays())
        self.assertIn(student1, upcoming_birthdays)
        self.assertNotIn(student2, upcoming_birthdays)


class UserAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_teacher_admin_display(self):
        teacher = Teacher.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com'
        )
        teacher_admin = TeacherAdmin(Teacher, self.site)
        self.assertEqual(teacher_admin.get_list_display(None), ('first_name', 'last_name'))

    def test_parent_admin_display(self):
        parent = Parent.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com'
        )
        parent_admin = ParentAdmin(Parent, self.site)
        self.assertEqual(parent_admin.get_list_display(None), ('first_name', 'last_name', 'email', 'students_list'))

    def test_student_admin_display(self):
        student = Student.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com'
        )
        student_admin = StudentAdmin(Student, self.site)
        self.assertEqual(student_admin.get_list_display(None), ('first_name', 'last_name', 'display_classes'))
