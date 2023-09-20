import os
from django.shortcuts import render, redirect, reverse
from django.views.generic import UpdateView
from bs4 import BeautifulSoup
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from teacher import models as TMODEL
from student import models as SMODEL
from teacher import forms as TFORM
from student import forms as SFORM
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Question
from django.http import HttpResponse
from django.contrib.auth import logout
from openpyxl import Workbook
from django.utils.encoding import smart_str

def handling_404(request,exception):
    return render(request, '404.html', {})

def handling_500(request):
    return render(request, '500.html')

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'quiz/index.html')


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


def afterlogin_view(request):
    if is_student(request.user):
        return redirect('student/student-dashboard')

    elif is_teacher(request.user):
        accountapproval = TMODEL.Teacher.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('teacher/teacher-dashboard')
        else:
            return render(request, 'teacher/teacher_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def admin_dashboard_view(request):
    dict = {
        'total_student': SMODEL.Student.objects.all().count(),
        'total_teacher': TMODEL.Teacher.objects.all().filter(status=True).count(),
        'total_course': models.Course.objects.all().count(),
        'total_question': models.Question.objects.all().count(),
    }
    return render(request, 'quiz/admin_dashboard.html', context=dict)


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def admin_teacher_view(request):
    dict = {
        'total_teacher': TMODEL.Teacher.objects.all().filter(status=True).count(),
        'pending_teacher': TMODEL.Teacher.objects.all().filter(status=False).count(),
        'salary': TMODEL.Teacher.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    }
    return render(request, 'quiz/admin_teacher.html', context=dict)


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def admin_view_teacher_view(request):
    teachers = TMODEL.Teacher.objects.all().filter(status=True).order_by('course')
    return render(request, 'quiz/admin_view_teacher.html', {'teachers': teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def update_teacher_view(request, pk):
    teacher = TMODEL.Teacher.objects.get(id=pk)
    user = TMODEL.User.objects.get(id=teacher.user_id)
    userForm = TFORM.TeacherUserForm(instance=user)
    teacherForm = TFORM.TeacherForm(instance=teacher)
    mydict = {'userForm': userForm, 'teacherForm': teacherForm}
    if request.method == 'POST':
        userForm = TFORM.TeacherUserForm(request.POST, instance=user)
        teacherForm = TFORM.TeacherForm(request.POST, instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            teacherForm.save()
            return redirect('admin-view-teacher')
    return render(request, 'quiz/update_teacher.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def delete_teacher_view(request, pk):
    teacher = TMODEL.Teacher.objects.get(id=pk)
    print(teacher)
    user = User.objects.get(id=teacher.user_id)
    # print(user.)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def admin_view_pending_teacher_view(request):
    teachers = TMODEL.Teacher.objects.all().filter(status=False)
    return render(request, 'quiz/admin_view_pending_teacher.html', {'teachers': teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def approve_teacher_view(request, pk):
    teacherSalary = forms.TeacherSalaryForm()
    if request.method == 'POST':
        teacherSalary = forms.TeacherSalaryForm(request.POST)
        if teacherSalary.is_valid():
            teacher = TMODEL.Teacher.objects.get(id=pk)
            teacher.salary = teacherSalary.cleaned_data['salary']
            teacher.status = True
            teacher.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-pending-teacher')
    return render(request, 'quiz/salary_form.html', {'teacherSalary': teacherSalary})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def reject_teacher_view(request, pk):
    teacher = TMODEL.Teacher.objects.get(id=pk)
    user = User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-pending-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def admin_view_teacher_salary_view(request):
    teachers = TMODEL.Teacher.objects.all().filter(status=True)
    return render(request, 'quiz/admin_view_teacher_salary.html', {'teachers': teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def admin_student_view(request):
    dict = {
        'total_student': SMODEL.Student.objects.all().count(),
    }
    return render(request, 'quiz/admin_student.html', context=dict)


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def admin_view_student_view(request):
    students = SMODEL.Student.objects.all().order_by('-classes')
    return render(request, 'quiz/admin_view_student.html', {'students': students})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def update_student_view(request, pk):
    student = SMODEL.Student.objects.get(id=pk)
    user = SMODEL.User.objects.get(id=student.user_id)
    userForm = SFORM.StudentUserForm(instance=user)
    studentForm = SFORM.StudentForm(instance=student)
    mydict = {'userForm': userForm, 'studentForm': studentForm}
    if request.method == 'POST':
        userForm = SFORM.StudentUserForm(request.POST, instance=user)
        studentForm = SFORM.StudentForm(request.POST, instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('admin-view-student')
        else:
            mydict = {'userForm': userForm, 'studentForm': studentForm}

    return render(request, 'quiz/update_student.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def delete_student_view(request, pk):
    student = SMODEL.Student.objects.get(id=pk)
    user = User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-student')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def admin_course_view(request):
    return render(request, 'quiz/admin_course.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def admin_add_course_view(request):
    courseForm = forms.CourseForm()
    if request.method == 'POST':
        courseForm = forms.CourseForm(request.POST)
        if courseForm.is_valid():
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-course')
    return render(request, 'quiz/admin_add_course.html', {'courseForm': courseForm})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def admin_view_course_view(request):
    courses = models.Course.objects.all()
    return render(request, 'quiz/admin_view_course.html', {'courses': courses})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def delete_course_view(request, pk):
    course = models.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/admin-view-course')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def admin_question_view(request):
    return render(request, 'quiz/admin_question.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def admin_view_question_view(request):
    courses = models.Course.objects.all()
    return render(request, 'quiz/admin_view_question.html', {'courses': courses})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def view_question_view(request, pk):
    questions = models.Question.objects.all().filter(course_id=pk).order_by('-classes')
    return render(request, 'quiz/view_question.html', {'questions': questions})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def admin_view_students_course(request):
    course = models.Course.objects.all()
    return render(request, 'quiz/admin_view_students_course.html', {'course': course})

@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def admin_view_classes_results(request, pk):
    classes = models.Classes.objects.all()
    response = render(request, 'quiz/admin_view_classes_results.html', {'classes': classes})
    response.set_cookie('course_id', str(pk))
    return response

@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def download_students_results(request,classes_id):
    # Students ro'yxatini olish (sizning tadbirlogikangizga qarab)
    class_id = models.Classes.objects.filter(id=classes_id).first()
    course_id = request.COOKIES.get('course_id')
    selected_course = get_object_or_404(models.Course, pk=course_id)
    course_name = selected_course.course_name
    students = SMODEL.Student.objects.filter(classes=class_id)
    wb = Workbook()
    ws = wb.active

    # Excel fayl ustunlarini qo'shish
    ws.append(['Ism', 'Familiya', 'Kurs', 'Ball', 'Test bajarilgan vaqt', 'Sinf raqami'])

    for student in students:
        latest_result = models.Result.objects.filter(student=student,course=selected_course).order_by('-date').first()
        if latest_result:
            new_date = latest_result.date + timedelta(hours=5)

            data = [
                student.user.first_name,
                student.user.last_name,
                latest_result.course.course_name,
                latest_result.marks,
                new_date.strftime('%Y-%m-%d %H:%M:%S'),  # Besh soatni qo'shish
                latest_result.classes.class_name,
            ]

            # Excel faylga qo'shish
            ws.append(data)

    # Excel faylni saqlash
    filename = f'{class_id}_{course_name}_natijalar.xlsx'
    wb.save(filename)

    with open(filename, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={smart_str(filename)}'
    if os.path.exists(filename):
        os.remove(filename)

    return response



@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def admin_check_marks_view(request, pk):
    course = models.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student = SMODEL.Student.objects.get(id=student_id)

    results = models.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request, 'quiz/admin_update_course.html', {'results': results})


def aboutus_view(request):
    return render(request, 'quiz/aboutus.html')


def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']

            send_mail(str(f'Ismi: {name}') + ' || ' + str(f' Emaili: {email}'), message, settings.EMAIL_HOST_USER,
                      [settings.ADMIN_EMAIL],
                      fail_silently=False)
            return render(request, 'quiz/contactussuccess.html')
    return render(request, 'quiz/contactus.html', {'form': sub})


class QuestionUpdateViewAdmin(UpdateView):
    model = Question
    template_name = 'quiz/question_update.html'
    fields = ['marks', 'question', 'variant_A', 'variant_B', 'variant_C', 'variant_D', 'answer']

    success_url = '/admin-view-question'


class QuestionUpdateViewTeacher(UpdateView):
    model = Question
    template_name = 'teacher/update_question_teacher.html'
    fields = ['classes', 'marks', 'question', 'variant_A', 'variant_B', 'variant_C', 'variant_D', 'answer']

    success_url = '/teacher/teacher-view-question'

    def form_valid(self, form):
        question = form.save(commit=False)

        if question.teacher == self.request.user.pk:
            question.save()
            messages.success(self.request, 'Savol muvaffaqiyatli yangilandi!')
            return super().form_valid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('see-question', kwargs={'class_id': self.object.classes.id})


def clear_all_cookies(request):
    # Foydalanuvchi (user) session ma'lumotlarini tozalash
    request.session.flush()

    # Barcha cookielarni o'chirish
    response = redirect("/logout")  # Buni o'zingizga mos xabar qo'ying
    for key in request.COOKIES:
        # Bo'sh joylarni o'chirish
        if key.strip():  # Bo'sh joylarni tekshirish
            response.delete_cookie(key)

    # Logout qilish
    logout(request)

    return response



@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def admin_update_courses(request):
    course = models.Course.objects.all()
    return render(request, 'quiz/admin_update_course.html', {'course': course})


@login_required(login_url='adminlogin')
@user_passes_test(is_staff_user)
def admin_update_click_course(request, pk):
    course = get_object_or_404(models.Course, id=pk)

    if request.method == 'POST':
        form = forms.UpdateCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin-update-courses')
    else:
        form = forms.UpdateCourseForm(instance=course)

    return render(request, 'quiz/admin_update_click_course.html', {'form': form, 'course': course})