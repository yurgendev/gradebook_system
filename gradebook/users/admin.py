from django.contrib import admin
from .models import Teacher, Parent, Student


class HideLastLoginMixin:
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields.pop('last_login', None)
        return form


@admin.register(Teacher)
class TeacherAdmin(HideLastLoginMixin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'display_class')
    list_display_links = ('first_name', 'last_name')
    search_fields = ['first_name', 'last_name']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('class_teacher')

    def display_class(self, obj):
        class_teacher = obj.class_teacher.first()
        if class_teacher:
            return class_teacher.class_name
        return ''

    display_class.short_description = 'Class'


@admin.register(Parent)
class ParentAdmin(HideLastLoginMixin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'students_list')
    list_editable = ('email',)
    list_display_links = ('first_name', 'last_name')
    search_fields = ['first_name', 'last_name']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('children')

    def students_list(self, obj):
        return ", ".join([str(student) for student in obj.children.all()])

    students_list.short_description = 'Students'


@admin.register(Student)
class StudentAdmin(HideLastLoginMixin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'display_classes')
    # list_filter = ('classes__name',)
    list_display_links = ('first_name', 'last_name')
    search_fields = ['first_name', 'last_name']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('classes')

    def display_classes(self, obj):
        return ", ".join([str(school_class) for school_class in obj.classes.all()])

    display_classes.short_description = 'Classes'
