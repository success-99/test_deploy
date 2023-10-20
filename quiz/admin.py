from django.contrib import admin
from .models import Course, Question, Classes, Result, RandomQuestionMarks

# Register your models here.

admin.site.register(Classes)
admin.site.register(Course)
admin.site.register(Question)
admin.site.register(RandomQuestionMarks)


@admin.register(Result)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'date']

# Register your models here.
