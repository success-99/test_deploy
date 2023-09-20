from django.contrib import admin
from .models import Teacher
# Register your models here.


@admin.register(Teacher)
class AuthorTeacher(admin.ModelAdmin):
    list_display = ['course']