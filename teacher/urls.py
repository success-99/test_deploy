from django.urls import path,include
from teacher import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ckeditor_views


urlpatterns = [
    path('teacherclick', views.teacherclick_view),
    path('teacherlogin', LoginView.as_view(template_name='teacher/teacherlogin.html'), name='teacherlogin'),
    path('teachersignup', views.teacher_signup_view, name='teachersignup'),
    path('teacher-dashboard', views.teacher_dashboard_view, name='teacher-dashboard'),
    path('teacher-exam', views.teacher_exam_view, name='teacher-exam'),
    path('teacher-add-exam', views.teacher_add_exam_view, name='teacher-add-exam'),
    path('teacher-view-exam', views.teacher_view_exam_view, name='teacher-view-exam'),
    path('delete-exam/<int:pk>', views.delete_exam_view, name='delete-exam'),

    path('teacher-student', views.tech_student_view, name='teacher-student'),
    path('teacher-view-student-marks', views.tech_view_student_marks_view, name='teacher-view-student-marks'),
    path('teacher-view-marks/<int:pk>', views.tech_view_marks_view, name='teacher-view-marks'),
    path('teacher-check-marks/<int:pk>', views.tech_check_marks_view, name='teacher-check-marks'),

    path('teacher-question', views.teacher_question_view, name='teacher-question'),
    path('teacher-add-question', views.teacher_add_question_view, name='teacher-add-question'),
    path('teacher-view-question', views.teacher_view_question_view, name='teacher-view-question'),
    path('see-question/<int:pk>', views.see_question_view, name='see-question'),
    path('remove-question/<int:pk>', views.remove_question_view, name='remove-question'),

]
