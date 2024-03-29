from django.urls import path
from student import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('studentclick', views.studentclick_view),
    path('studentlogin', LoginView.as_view(template_name='student/studentlogin.html'), name='studentlogin'),
    path('studentsignup', views.student_signup_view, name='studentsignup'),
    path('student-dashboard', views.student_dashboard_view, name='student-dashboard'),
    path('student-teachers', views.student_teachers_view, name='student-teachers'),
    path('student-exam', views.student_exam_view, name='student-exam'),
    path('take-exam/<uuid:pk>', views.take_exam_view, name='take-exam'),
    path('start-exam/<uuid:pk>', views.start_exam_view, name='start-exam'),
    path('calculate-marks', views.calculate_marks_view, name='calculate-marks'),
    path('check-marks/<uuid:pk>', views.check_marks_view, name='check-marks'),
    path('student-marks', views.student_marks_view, name='student-marks'),
]
