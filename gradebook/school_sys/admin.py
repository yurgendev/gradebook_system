from django.contrib import admin
from .models import SchoolClass, Lesson, Grade


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'class_teacher', 'display_students',)
    list_display_links = ('class_name',)
    search_fields = ['class_name', 'class_teacher__first_name', 'class_teacher__last_name', 'students__first_name', 'students__last_name']
    list_filter = ['class_teacher', 'students']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('students').order_by('students__last_name', 'students__first_name')

    def display_students(self, obj):
        return ", ".join([student.first_name for student in obj.students.all()])

    display_students.short_description = 'Students'



@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    pass
