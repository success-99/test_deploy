from django.db import models
from django.contrib.auth.models import User, PermissionsMixin
from quiz.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
# from .utils import send_registration_notification_email

# from .bot import send_telegram_message


class Student(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classes = models.ForeignKey("quiz.Classes", on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20, null=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.user.first_name


# @receiver(post_save, sender=Student)
# def student_registration_handler(sender, instance, created, **kwargs):
#     if created:
#         # Yangi student ro'yxatdan o'tgan
#         classes_count = Student.objects.filter(user__is_active=True).count()
#         send_registration_notification_email(classes_count)