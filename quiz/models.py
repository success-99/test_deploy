from django.db import models
from student.models import Student
from teacher.models import Teacher
from ckeditor_uploader.fields import RichTextUploadingField


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    question_number = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()

    def __str__(self):
        return self.course_name


class Question(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,related_name='questions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    question = RichTextUploadingField(null=True, blank=True)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    cat = (('Option1', 'Option1'), ('Option2', 'Option2'), ('Option3', 'Option3'), ('Option4', 'Option4'))
    answer = models.CharField(max_length=200, choices=cat)


    def check_teacher_question(self,user):
        print(self.teacher.user==user)
        return self.teacher.user==user






    def __str__(self):
        return self.question


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
