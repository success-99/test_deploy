from django.urls import path, include
from django.contrib import admin
from rest_framework import permissions

from quiz import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView, LoginView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ckeditor_views

from quiz.views import QuestionUpdateViewTeacher, QuestionUpdateViewAdmin

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)
urlpatterns = [

                  path('admin/', admin.site.urls),
                  path('swagger<format>.json|.yaml', schema_view.without_ui(cache_timeout=0), name='schema-json'),
                  path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

                  # path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
                  path('ckeditor/browse/', never_cache(login_required(ckeditor_views.browse)), name='ckeditor_browse'),
                  path('teacher/', include('teacher.urls')),
                  path('student/', include('student.urls')),

                  path('', views.home_view, name=''),
                  path('logout', LogoutView.as_view(template_name='quiz/logout.html'), name='logout'),
                  path('aboutus', views.aboutus_view),
                  path('contactus', views.contactus_view),
                  path('afterlogin', views.afterlogin_view, name='afterlogin'),

                  path('adminclick', views.adminclick_view),
                  path('adminlogin', LoginView.as_view(template_name='quiz/adminlogin.html'), name='adminlogin'),
                  path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),
                  path('admin-teacher', views.admin_teacher_view, name='admin-teacher'),
                  path('admin-view-teacher', views.admin_view_teacher_view, name='admin-view-teacher'),
                  path('update-teacher/<int:pk>', views.update_teacher_view, name='update-teacher'),
                  path('delete-teacher/<int:pk>', views.delete_teacher_view, name='delete-teacher'),
                  path('admin-view-pending-teacher', views.admin_view_pending_teacher_view,
                       name='admin-view-pending-teacher'),
                  path('admin-view-teacher-salary', views.admin_view_teacher_salary_view,
                       name='admin-view-teacher-salary'),
                  path('approve-teacher/<int:pk>', views.approve_teacher_view, name='approve-teacher'),
                  path('reject-teacher/<int:pk>', views.reject_teacher_view, name='reject-teacher'),

                  path('admin-student', views.admin_student_view, name='admin-student'),
                  path('admin-view-student', views.admin_view_student_view, name='admin-view-student'),
                  path('admin-view-student-marks', views.admin_view_student_marks_view,
                       name='admin-view-student-marks'),
                  path('admin-view-marks/<int:pk>', views.admin_view_marks_view, name='admin-view-marks'),
                  path('admin-check-marks/<int:pk>', views.admin_check_marks_view, name='admin-check-marks'),
                  path('update-student/<int:pk>', views.update_student_view, name='update-student'),
                  path('delete-student/<int:pk>', views.delete_student_view, name='delete-student'),

                  path('admin-course', views.admin_course_view, name='admin-course'),
                  path('admin-add-course', views.admin_add_course_view, name='admin-add-course'),
                  path('admin-view-course', views.admin_view_course_view, name='admin-view-course'),
                  path('delete-course/<int:pk>', views.delete_course_view, name='delete-course'),

                  path('admin-question', views.admin_question_view, name='admin-question'),
                  path('admin-add-question', views.admin_add_question_view, name='admin-add-question'),
                  path('admin-view-question', views.admin_view_question_view, name='admin-view-question'),
                  path('view-question/<int:pk>', views.view_question_view, name='view-question'),
                  path('update-question/<int:pk>', QuestionUpdateViewAdmin.as_view(), name='update-question-admin'),
                  path('update-question/teacher/<int:pk>', QuestionUpdateViewTeacher.as_view(), name='update-question-teacher'),
                  path('delete-question/<int:pk>', views.delete_question_view, name='delete-question'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
