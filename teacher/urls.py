from django.urls import path
from teacher import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('teacherclick', views.teacherclick_view),
    path('teacherlogin', LoginView.as_view(template_name='teacher/teacherlogin.html'), name='teacherlogin'),
    path('teachersignup', views.teacher_signup_view, name='teachersignup'),
    path('teacher-dashboard', views.teacher_dashboard_view, name='teacher-dashboard'),
    path('teacher-class', views.teacher_class_view, name='teacher-class'),
    path('teacher-view-class-student/<uuid:class_id>', views.tech_classes_student_view, name='teacher-classes-student'),
    path('download_student_results', views.download_student_results, name='download_student_results'),
    path('teacher-view-class-student-date/<uuid:student_id>', views.tech_view_class_student_date,
         name='teacher-view-class-student-date'),
    path('teacher-student-result-view/<uuid:result_id>', views.teacher_student_result_view,
         name='teacher-student-result'),

    path('teacher-add-exam', views.teacher_add_exam_view, name='teacher-add-exam'),
    path('teacher-view-exam', views.teacher_view_exam_view, name='teacher-view-exam'),
    path('delete-exam/<uuid:pk>', views.delete_exam_view, name='delete-exam'),

    path('teacher-update-profile', views.update_profile, name='teacher-update-profile'),
    path('teacher-view-student-marks', views.tech_view_student_marks_view, name='teacher-view-student-marks'),

    path('teacher-question', views.teacher_question_view, name='teacher-question'),
    path('teacher-add-question', views.teacher_add_question_view, name='teacher-add-question'),
    path('teacher-view-question', views.teacher_view_question_view, name='teacher-view-question'),
    path('see-question/<uuid:class_id>', views.see_question_view, name='see-question'),
    path('remove-question/<uuid:pk>', views.remove_question_view, name='remove-question'),
    path('remove-result/<uuid:pk>', views.remove_result_view, name='remove-result'),

    path('update-course', views.tech_update_course, name='update-course'),
    path('student-class-update/<uuid:student_id>', views.student_class_update, name='student-class-update'),

    path('teacher-view-question-number', views.teacher_view_question_random, name='teacher-view-question-random'),
    path('teacher-add-random-number/<uuid:class_id>', views.teacher_random_question_marks, name='teacher-random-question-marks'),

]
