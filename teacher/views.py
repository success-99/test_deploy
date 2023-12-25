from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import timedelta
from quiz import models as QMODEL
from student import models as SMODEL
from quiz import forms as QFORM
from teacher.models import Teacher
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
import os
from bs4 import BeautifulSoup
from openpyxl import Workbook
from django.http import HttpResponse
from django.utils.encoding import smart_str
from student.forms import StudentClassUpdateForm


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

#def
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    user = request.user
    teacher = Teacher.objects.get(user=user)

    dict = {

        'teacher_course': teacher.course.course_name,
        'total_course': QMODEL.Course.objects.all().count(),
        'total_question': QMODEL.Question.objects.filter(teacher=teacher).count(),
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


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def tech_classes_student_view(request, class_id):
    teacher = Teacher.objects.get(user=request.user)
    tech_course = teacher.course.course_name
    tech_course_id = teacher.course.id
    selected_class = QMODEL.Classes.objects.get(pk=class_id)
    students = SMODEL.Student.objects.filter(classes=selected_class)
    student_count = students.count()

    response = render(request, 'teacher/tech_classes_student_view.html', {
        'selected_class': selected_class,
        'students': students,
        'course_name': tech_course,
        'student_count': student_count,
    })
    response.set_cookie('class_id', class_id)
    response.set_cookie('course_id', tech_course_id)

    return response


# @login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def download_student_results_teacher(request):
    # Students ro'yxatini olish (sizning tadbirlogikangizga qarab)
    class_id = request.COOKIES.get('class_id')
    selected_class = get_object_or_404(QMODEL.Classes, pk=class_id)
    course_id = request.COOKIES.get('course_id')
    selected_course = get_object_or_404(QMODEL.Course, pk=course_id)
    class_name = selected_class.class_name
    course_name = selected_course.course_name
    students = SMODEL.Student.objects.filter(classes=selected_class)
    wb = Workbook()
    ws = wb.active

    # Excel fayl ustunlarini qo'shish
    ws.append(['Ism', 'Familiya', 'Kurs', 'Ball', 'Test bajarilgan vaqt', 'Sinf raqami'])

    for student in students:
        latest_result = QMODEL.Result.objects.filter(student=student, course=selected_course).order_by('-date').first()
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
    filename = f'{class_name}_{course_name}_natijalar.xlsx'
    wb.save(filename)

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
    results = QMODEL.Result.objects.filter(student=student, course=tech_course_id, classes=classes).order_by('date')
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
        form = forms.UpdateCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/teacher/teacher-dashboard')
    else:
        form = forms.UpdateCourseForm(instance=course)

    return render(request, 'teacher/tech_update_course.html', {'form': form, 'course': course})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def update_profile(request):
    teacher = Teacher.objects.get(user=request.user)
    user = User.objects.get(id=teacher.user_id)
    userForm = forms.TeacherUserForm(instance=user)
    # teacherForm = forms.TeacherUForm(instance=teacher)
    initial_course = teacher.course.id if teacher.course else None
    teacherForm = forms.TeacherUForm(instance=teacher, initial={'course': initial_course})
    mydict = {'userForm': userForm, 'teacherForm': teacherForm}
    if request.method == 'POST':
        userForm = forms.TeacherUserForm(request.POST, instance=user)
        teacherForm = forms.TeacherUForm(request.POST, instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            teacherForm.save()
            new_course = teacherForm.cleaned_data.get('course')

            # Eski kursni olish
            old_course = teacher.course

            # Kurs o'zgarmagan bo'lsa va yangi kurs tanlangan bo'lsa
            if old_course != new_course and new_course is not None:
                teacher.course = new_course
                teacher.status = False  # statusni "False" qilamiz

            teacherForm.save()
            return redirect('/teacher/teacherlogin')

    return render(request, 'teacher/teacher_profile.html', context=mydict)


def student_class_update(request, student_id):
    student = get_object_or_404(SMODEL.Student, id=student_id)
    classid = request.COOKIES.get('class_id')
    if request.method == 'POST':
        form = StudentClassUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('teacher-classes-student',
                            class_id=classid)  # O'zgartirilgan studentni ko'rsatish uchun mos manzil
    else:
        form = StudentClassUpdateForm(instance=student)

    return render(request, 'student/student_class_update.html', {'form': form, 'student': student})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_question_random(request):
    teacher = Teacher.objects.get(user=request.user)
    course_id = teacher.course.id
    courses = QMODEL.Course.objects.all().filter(id=course_id)
    classes = QMODEL.Classes.objects.all()
    response = render(request, 'teacher/teacher_view_question_random.html', {'courses': courses, 'classes': classes})
    response.set_cookie('course_id',course_id)

    return response


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_random_question_marks(request, class_id):
    classes = QMODEL.Classes.objects.get(id=class_id)
    course_id = request.COOKIES.get('course_id')
    random_n = QMODEL.RandomQuestionMarks.objects.all().filter(classes=classes, course=course_id).first()
    question_count = QMODEL.Question.objects.filter(course=course_id, classes=classes).count()
    if request.method == 'POST':
        questionRandomForm = QFORM.RandomQuestionMarksForm(request.POST, instance=random_n)
        if questionRandomForm.is_valid():
            question_random = questionRandomForm.save(commit=False)
            teacher = Teacher.objects.get(user=request.user)
            course_id = str(teacher.course.id)
            course = QMODEL.Course.objects.get(id=course_id)
            classes = QMODEL.Classes.objects.get(id=class_id)
            marks = question_random.marks
            question_count = QMODEL.Question.objects.filter(course=course, classes=classes).count()
            if marks <= question_count:
                question_random.course = course
                question_random.classes = classes
                question_random.save()
                return HttpResponseRedirect('/teacher/teacher-view-question-number')
            else:
                messages.error(request, "Nato'g'ri son kiritdingiz!!!")
        else:
            print("Form is invalid")
    else:
        questionRandomForm = QFORM.RandomQuestionMarksForm(instance=random_n)
    return render(request, 'teacher/teacher_add_question_num.html', {'form': questionRandomForm, 'classes': classes, 'que_c': question_count})
