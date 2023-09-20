from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from teacher import models as TMODEL
from student import models as SMODEL
from django.contrib import messages


# for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'student/studentclick.html')


def student_signup_view(request):
    userForm = forms.StudentUserForm()
    studentForm = forms.StudentForm()
    mydict = {'userForm': userForm, 'studentForm': studentForm}
    if request.method == 'POST':
        userForm = forms.StudentUserForm(request.POST)
        studentForm = forms.StudentForm(request.POST)
        studentForm.instance.classes_id = request.POST.get('classes')
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            student = studentForm.save(commit=False)
            student.user = user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
            return HttpResponseRedirect('studentlogin')
        else:
            mydict['userForm'] = userForm
            mydict['studentForm'] = studentForm
    return render(request, 'student/studentsignup.html', context=mydict)


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    user = request.user
    student = models.Student.objects.get(user=user)
    dict = {
        'student_class': student.classes.class_name,
        'total_course': QMODEL.Course.objects.all().count(),
        'total_question': QMODEL.Question.objects.all().count(),
    }
    return render(request, 'student/student_dashboard.html', context=dict)


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/student_exam.html', {'courses': courses})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request, pk):
    student = models.Student.objects.get(user=request.user)
    classes_id = student.classes.id
    course = QMODEL.Course.objects.get(id=pk)
    total_questions = QMODEL.Question.objects.all().filter(course=course, classes=classes_id).count()
    questions = QMODEL.Question.objects.all().filter(course=course, classes=classes_id)
    total_marks = 0
    for q in questions:
        total_marks = total_marks + q.marks
    response = render(request, 'student/take_exam.html',
                  {'course': course, 'total_questions': total_questions, 'total_marks': total_marks})
    response.set_cookie('course_id', course.id)
    return response



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request, pk):
    student = models.Student.objects.get(user=request.user)
    classes_id = student.classes.id
    course = QMODEL.Course.objects.get(id=pk)
    questions = QMODEL.Question.objects.all().filter(course=course, classes=classes_id)
    if not course.status:
        messages.error(request, "Bu imtihon hali faollashtirilmagan")

        return HttpResponse("Bu kurs hali faollashtirilmagan")

    if 'clear_cookies' in request.GET and request.GET['clear_cookies'] == '1':
        response = render(request, 'student/start_exam.html', {'course': course, 'questions': questions})
        for i in range(len(questions)):
            response.delete_cookie(str(i + 1))
        return response

    if request.method == 'POST':
        pass
    response = render(request, 'student/start_exam.html', {'course': course, 'questions': questions})
    if request.COOKIES.get('course_id') is None:
        response.set_cookie('course_id', course.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course = QMODEL.Course.objects.get(id=course_id)
        student = models.Student.objects.get(user_id=request.user.id)
        classes_id = student.classes
        total_marks = 0
        questions = QMODEL.Question.objects.all().filter(course=course, classes=classes_id)
        question_results = []

        for i in range(len(questions)):
            actual_answer = questions[i].answer
            selected_ans = request.COOKIES.get(str(i + 1))
            if actual_answer == selected_ans and selected_ans is not None:
                total_marks = total_marks + questions[i].marks
            if selected_ans is None:
                selected_ans = 'belgilanmagan'
            if selected_ans != actual_answer:
                question_results.append({
                    'question': questions[i].question,
                    'selected_answer': selected_ans,
                    'correct_answer': actual_answer
                })
        student_classes = student.classes
        result = QMODEL.Result()
        result.marks = total_marks
        result.course = course
        result.student = student
        result.classes = student_classes  # O'quvchining classes qiymatini saqlash
        result.question_results = question_results
        result.save()
        return HttpResponseRedirect('student-marks')


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/view_result.html', {'courses': courses})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    course_t_m = course.total_marks
    student = models.Student.objects.get(user_id=request.user.id)
    results = QMODEL.Result.objects.all().filter(course=course).filter(student=student).order_by('date')
    return render(request, 'student/check_marks.html', {'results': results, 'total_marks': course_t_m})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/student_marks.html', {'courses': courses})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_teachers_view(request):
    teachers = TMODEL.Teacher.objects.all()
    return render(request, 'student/student_teachers.html', {'teachers': teachers})
