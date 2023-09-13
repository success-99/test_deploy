from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from student import models as SMODEL
from quiz import forms as QFORM
from teacher.models import Teacher
from django.shortcuts import get_object_or_404
from .forms import UpdateCourseForm, CombinedTeacherUpdateForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import UpdateView
import os
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import Workbook
import datetime
from django.http import HttpResponse
from django.utils.encoding import smart_str
import time


# for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'teacher/teacherclick.html')


def teacher_signup_view(request):
    userForm = forms.TeacherUserForm()
    teacherForm = forms.TeacherForm()
    mydict = {'userForm': userForm, 'teacherForm': teacherForm}
    if request.method == 'POST':
        userForm = forms.TeacherUserForm(request.POST)
        teacherForm = forms.TeacherForm(request.POST)
        teacherForm.instance.course_id = request.POST.get('course')
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            teacher = teacherForm.save(commit=False)
            teacher.user = user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
            return HttpResponseRedirect('teacherlogin')
        else:
            mydict['userForm'] = userForm
            mydict['studentForm'] = teacherForm
    return render(request, 'teacher/teachersignup.html', context=mydict)


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    user = request.user
    teacher = Teacher.objects.get(user=user)
    dict = {

        'teacher_course': teacher.course.course_name,
        'total_course': QMODEL.Course.objects.all().count(),
        'total_question': QMODEL.Question.objects.all().count(),
        'total_student': SMODEL.Student.objects.all().count()
    }
    return render(request, 'teacher/teacher_dashboard.html', context=dict)


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_class_view(request):
    user = request.user
    teacher = Teacher.objects.get(user=user)
    classes = QMODEL.Classes.objects.all()
    return render(request, 'teacher/teacher_class.html',
                  {'classes': classes, 'teacher_course': teacher.course.course_name})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_exam_view(request):
    courseForm = QFORM.CourseForm()
    if request.method == 'POST':
        courseForm = QFORM.CourseForm(request.POST)
        if courseForm.is_valid():
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-exam')
    return render(request, 'teacher/teacher_add_exam.html', {'courseForm': courseForm})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_exam_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'teacher/teacher_view_exam.html', {'courses': courses})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_exam_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')


@login_required(login_url='teacherlogin')
def tech_view_student_marks_view(request):
    students = SMODEL.Student.objects.all()
    return render(request, 'teacher/tech_view_student_marks.html', {'students': students})


#
# @login_required(login_url='teacherlogin')
# def tech_view_marks_view(request, pk):
#     courses = QMODEL.Course.objects.all()
#     response = render(request, 'teacher/tech_view_marks.html', {'courses': courses})
#     response.set_cookie('student_id', str(pk))
#     return response


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def tech_classes_student_view(request, class_id):
    teacher = Teacher.objects.get(user=request.user)
    tech_course = teacher.course.course_name
    selected_class = QMODEL.Classes.objects.get(pk=class_id)
    students = SMODEL.Student.objects.filter(classes=selected_class)
    student_count = students.count()

    students = SMODEL.Student.objects.filter(classes=selected_class)
    wb = Workbook()
    ws = wb.active

    # Excel fayl ustunlarini qo'shish
    ws.append(['Ism', 'Familiya', 'Kurs', 'Ball', 'Test bajarilgan vaqt'])

    for student in students:
        # Har bir studentning oxirgi natijalarini olish
        latest_result = QMODEL.Result.objects.filter(student=student).order_by('-date').first()

        if latest_result:
            new_date = latest_result.date + datetime.timedelta(hours=5)

            data = [
                student.user.first_name,
                student.user.last_name,
                latest_result.course.course_name,
                latest_result.marks,
                new_date.strftime('%Y-%m-%d %H:%M:%S'),  # Besh soatni qo'shish
            ]

            # Excel faylga qo'shish
            ws.append(data)

    # Excel faylni saqlash
    filename = f'student_{selected_class}_results_latest_date.xlsx'
    wb.save(filename)

    context = {'selected_class': selected_class, 'students': students, 'course_name': tech_course,
               'student_count': student_count, 'filename': filename}
    return render(request, 'teacher/tech_classes_student_view.html', context)


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def download_student_results(request, filename):
    with open(filename, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={smart_str(filename)}'

        if os.path.exists(filename):
            os.remove(filename)
    return response


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_student_result_view(request, result_id):
    teacher = Teacher.objects.get(user=request.user)
    tech_course_id = teacher.course.id
    results = QMODEL.Result.objects.filter(id=result_id, course=tech_course_id)
    context = {'results': results}
    return render(request, 'teacher/tech_student_result.html', context)


@login_required(login_url='teacherlogin')
def tech_view_class_student_date(request, student_id):
    teacher = Teacher.objects.get(user=request.user)
    tech_course_id = teacher.course.id
    student = get_object_or_404(SMODEL.Student, pk=student_id)
    classes = student.classes.id
    results = QMODEL.Result.objects.filter(student=student, course=tech_course_id, classes=classes)
    context = {'student': student, 'results': results}
    return render(request, 'teacher/tech_classes_student_date_view.html', context)


@login_required(login_url='teacherlogin')
def teacher_question_view(request):
    return render(request, 'teacher/teacher_question.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_question_view(request):
    questionForm = QFORM.QuestionForm()
    if request.method == 'POST':
        questionForm = QFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            teacher = Teacher.objects.get(user=request.user)
            course_id = str(teacher.course.id)
            course = QMODEL.Course.objects.get(id=course_id)
            classes_id = request.POST.get('classes')
            classes = QMODEL.Classes.objects.get(id=classes_id)
            question.teacher = teacher
            question.course = course
            question.classes = classes
            question.save()
            return HttpResponseRedirect('/teacher/teacher-view-question')
        else:
            print("Form is invalid")
    return render(request, 'teacher/teacher_add_question.html', {'questionForm': questionForm})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_question_view(request):
    teacher = Teacher.objects.get(user=request.user)
    course_id = teacher.course.id
    courses = QMODEL.Course.objects.all().filter(id=course_id)
    classes = QMODEL.Classes.objects.all()
    return render(request, 'teacher/teacher_view_question.html', {'courses': courses, 'classes': classes})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_question_view(request, class_id):
    teacher = Teacher.objects.get(user=request.user)
    course_id = teacher.course.id
    questions = QMODEL.Question.objects.all().filter(classes=class_id, course=course_id)
    q_count = questions.count()
    t_marks = 0
    for q in questions:
        t_marks = t_marks + q.marks

    return render(request, 'teacher/see_question.html',
                  {'questions': questions, 'q_count': q_count, 't_marks': t_marks})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def remove_question_view(request, pk):
    question = QMODEL.Question.objects.get(id=pk)
    soup = BeautifulSoup(question.question, 'html.parser')
    img_tags = soup.find_all('img')

    for img_tag in img_tags:
        img_url = img_tag.get('src')[15:]  # .get() metodi ishlatilgan
        full_img_path = os.path.join(settings.MEDIA_ROOT, 'uploads', img_url)
        thumb_img_path = os.path.join(settings.MEDIA_ROOT, 'uploads',
                                      f'{img_url.split(".")[0]}_thumb.png')  # Thumb

        try:
            if os.path.exists(full_img_path):
                os.remove(full_img_path)
            if os.path.exists(thumb_img_path):
                os.remove(thumb_img_path)
        except Exception as e:
            messages.error(request, f"Xatolik: {str(e)}")

    question.delete()
    return redirect('see-question', class_id=question.classes.id)


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def remove_result_view(request, pk):
    results = QMODEL.Result.objects.get(id=pk)
    student_id = results.student.id
    results.delete()
    return redirect('teacher-view-class-student-date', student_id=student_id)


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def tech_update_course(request):
    teacher = Teacher.objects.get(user=request.user)
    course_id1 = teacher.course.id
    course = get_object_or_404(QMODEL.Course, id=course_id1)

    if request.method == 'POST':
        form = UpdateCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/teacher/teacher-dashboard')
    else:
        form = UpdateCourseForm(instance=course)

    return render(request, 'teacher/tech_update_course.html', {'form': form, 'course': course})


# @login_required(login_url='teacherlogin')
# @user_passes_test(is_teacher)
# def teacher_update_profile(request):
#     if request.method == 'POST':
#         user_form = TeacherUserUpdateForm(request.POST)
#         profile_form = TeacherUpdateForm(request.POST)
#         if user_form.is_valid() and profile_form.is_valid():
#             user = request.user
#             user.first_name = user_form.cleaned_data['first_name']
#             user.last_name = user_form.cleaned_data['last_name']
#             user.email = user_form.cleaned_data['email']
#             user.username = user_form.cleaned_data['username']
#             user.save()
#
#             teacher = request.user.teacher
#             teacher.mobile = profile_form.cleaned_data['mobile']
#             teacher.save()
#
#             messages.success(request, 'Your profile is updated successfully')
#             return redirect('/teacher/teacher-dashboard')
#     else:
#         user_form = TeacherUserUpdateForm(initial={
#             'first_name': request.user.first_name,
#             'last_name': request.user.last_name,
#             'email': request.user.email,
#             'username': request.user.username,
#         })
#         profile_form = TeacherUpdateForm(initial={
#             'mobile': request.user.teacher.mobile,
#         })
#     return render(request, 'teacher/teacher_profile.html', {'user_form': user_form, 'profile_form': profile_form})
#
# class TeacherUpdateProfil(UpdateView):
#     model = Teacher
#     template_name = 'teacher/teacher_profile.html'
#     fields = ['first_name', 'last_name', 'email', 'username', 'variant_B', 'variant_C', 'variant_D', 'answer']
#
#     success_url = '/teacher/teacher-view-question'
#
#     def form_valid(self, form):
#         question = form.save(commit=False)
#
#         if question.teacher == self.request.user.pk:
#             question.save()
#             messages.success(self.request, 'Savol muvaffaqiyatli yangilandi!')
#             return HttpResponseRedirect(self.get_success_url())
#         return super().form_valid(form)


# class TeacherProfileUpdateView(UpdateView):
#     model = Teacher
#     template_name = 'teacher/teacher_profile.html'
#     form_class = TeacherUpdateForm
#     success_url = '/teacher/teacher-dashboard'
#
#     def get_object(self, queryset=None):
#         return self.request.user.teacher
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user_form'] = TeacherUserUpdateForm()
#         return context

class TeacherProfileUpdateView(UpdateView):
    model = User
    template_name = 'teacher/teacher_profile.html'
    form_class = CombinedTeacherUpdateForm  # Yangi birlashtirilgan form
    success_url = '/teacher/teacher-dashboard'

    def get_object(self, queryset=None):
        return self.request.user.teacher
