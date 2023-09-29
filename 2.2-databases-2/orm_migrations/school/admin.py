from django.contrib import admin

from .models import Student, Teacher


class TeachersInline(admin.TabularInline):
    model = Student.teachers.through


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "group",]
    inlines = [
        TeachersInline,
    ]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    inlines = [
        TeachersInline,
    ]
    exclude = ('students',)
