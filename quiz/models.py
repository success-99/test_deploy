from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Classes(BaseModel):
    class_name = models.CharField(max_length=100)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.class_name


class Course(BaseModel):
    course_name = models.CharField(max_length=50)
    question_number = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.course_name


class Question(BaseModel):
    teacher = models.ForeignKey('teacher.Teacher', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    question = RichTextUploadingField()
    variant_A = RichTextUploadingField(default='A')
    variant_B = RichTextUploadingField(default='B')
    variant_C = RichTextUploadingField(default='C')
    variant_D = RichTextUploadingField(default='D')
    cat = (('variant_A', 'A'), ('variant_B', 'B'), ('variant_C', 'C'), ('variant_D', 'D'))
    answer = models.CharField(max_length=200, choices=cat)

    def __str__(self):
        return self.question


class Result(BaseModel):
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    question_results = models.JSONField(null=True)  # JSONField for question results
    date = models.DateTimeField(auto_now=True)
    c_marks = models.PositiveIntegerField(default=100)

    def __str__(self):
        return str(self.student)


class RandomQuestionMarks(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.course)


class CourseClassTime(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    times = models.IntegerField(
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(200)]
    )
