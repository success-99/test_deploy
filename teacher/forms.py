from django import forms
from django.contrib.auth.models import User
from . import models
from quiz.models import Course
from django.utils.translation import gettext_lazy as _


class TeacherUserForm(forms.ModelForm):
    con_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Bunday foydalanuvchi mavjud! Foydalanuvchi nomini o'zgartiring!")
        if len(username) < 4:
            raise forms.ValidationError(" Foydalanuvchi nomi 4 ta belgidan kam bo'lmasligi kerak!")
        if username.isdigit():  # Faqat sonlardan tashkil topganligini tekshirish
            raise forms.ValidationError("Foydalanuvchi nomi raqamlardan tashkil topishi munkin emas!")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name.isdigit():  # Faqat sonlardan tashkil topganligini tekshirish
            raise forms.ValidationError("Ismingiz raqamlardan tashkil topishi munkin emas!")
        if len(first_name) < 4:
            raise forms.ValidationError("Iltimos! Ismingiz 4 ta belgidan kam kiritmang!")
        if not first_name.isalpha():
            raise forms.ValidationError("Ismingiz faqat harflardan iborat bo'lishi kerak.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name.isdigit():  # Faqat sonlardan tashkil topganligini tekshirish
            raise forms.ValidationError("Familyangiz raqamlardan tashkil topishi munkin emas!")
        if len(last_name) < 4:
            raise forms.ValidationError("Iltimos! Familiyangizni 4 ta belgidan kam kiritmang!")
        if not last_name.isalpha():
            raise forms.ValidationError("Familiyangiz faqat harflardan iborat bo'lishi kerak.")
        return last_name

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 4 or len(password) > 8:
            raise forms.ValidationError(" Parolingiz 4 ta va 8 ta belgi oralig'ida bo'lishi kerak!")
        return password

    def clean_con_password(self):
        password = self.cleaned_data.get('password')  # get() ni ishlatamiz
        con_password = self.cleaned_data.get('con_password')
        if password and con_password and password != con_password:
            raise forms.ValidationError("Parollaringiz bir xil emas!")
        return con_password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            self.add_error("email", _("Bunday email egasi mavjud! Emailni o'zgartiring!"))
        return email


class TeacherForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="Fan nomi",
                                    to_field_name="id")

    class Meta:
        model = models.Teacher
        fields = ['mobile']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if models.Teacher.objects.filter(mobile__iexact=mobile).exists():
            self.add_error("mobile", _("Bunday telefon raqam egasi mavjud! Raqamingizni o'zgartiring!"))
        if not mobile:
            raise forms.ValidationError("Telefon raqamingizni kiriting.")
        if len(mobile) < 9 or len(mobile) > 13:
            raise forms.ValidationError("Telefon raqamingiz 9 ta va 13ta raqam oralig'ida bo'lishi kerak!.")
        if not mobile.isdigit():
            raise forms.ValidationError("Telefon raqam faqat sonlardan iborat bo'lishi kerak.")
        return mobile


class UpdateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['question_number', 'total_marks', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adding class to the status field to style it as a toggle switch
        self.fields['status'].widget.attrs.update({'class': 'toggle-switch'})


# class TeacherUserUpdateForm(forms.Form):
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'email']
#
#     def clean_username(self):
#         username = self.cleaned_data.get("username")
#         if User.objects.filter(username__iexact=username).exists():
#             raise forms.ValidationError("Bunday foydalanuvchi mavjud! Foydalanuvchi nomini o'zgartiring!")
#         if len(username) < 4:
#             raise forms.ValidationError(" Foydalanuvchi nomi 4 ta belgidan kam bo'lmasligi kerak!")
#         if username.isdigit():  # Faqat sonlardan tashkil topganligini tekshirish
#             raise forms.ValidationError("Foydalanuvchi nomi raqamlardan tashkil topishi munkin emas!")
#         return username
#
#     def clean_first_name(self):
#         first_name = self.cleaned_data.get('first_name')
#         if first_name.isdigit():  # Faqat sonlardan tashkil topganligini tekshirish
#             raise forms.ValidationError("Ismingiz raqamlardan tashkil topishi munkin emas!")
#         if len(first_name) < 4:
#             raise forms.ValidationError("Iltimos! Ismingiz 4 ta belgidan kam kiritmang!")
#         if not first_name.isalpha():
#             raise forms.ValidationError("Ismingiz faqat harflardan iborat bo'lishi kerak.")
#         return first_name
#
#     def clean_last_name(self):
#         last_name = self.cleaned_data.get('last_name')
#         if last_name.isdigit():  # Faqat sonlardan tashkil topganligini tekshirish
#             raise forms.ValidationError("Familyangiz raqamlardan tashkil topishi munkin emas!")
#         if len(last_name) < 4:
#             raise forms.ValidationError("Iltimos! Familiyangizni 4 ta belgidan kam kiritmang!")
#         if not last_name.isalpha():
#             raise forms.ValidationError("Familiyangiz faqat harflardan iborat bo'lishi kerak.")
#         return last_name
#
#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         if User.objects.filter(email__iexact=email).exists():
#             self.add_error("email", _("Bunday email egasi mavjud! Emailni o'zgartiring!"))
#         return email
#
#
# class TeacherUpdateForm(forms.ModelForm):
#     class Meta:
#         model = models.Teacher
#         fields = ['mobile']
#
#     def clean_mobile(self):
#         mobile = self.cleaned_data['mobile']
#         if models.Teacher.objects.filter(mobile__iexact=mobile).exists():
#             self.add_error("mobile", _("Bunday telefon raqam egasi mavjud! Raqamingizni o'zgartiring!"))
#         if not mobile:
#             raise forms.ValidationError("Telefon raqamingizni kiriting.")
#         if len(mobile) < 9 or len(mobile) > 13:
#             raise forms.ValidationError("Telefon raqamingiz 9 ta va 13ta raqam oralig'ida bo'lishi kerak!.")
#         if not mobile.isdigit():
#             raise forms.ValidationError("Telefon raqam faqat sonlardan iborat bo'lishi kerak.")
#         return mobile

class CombinedTeacherUpdateForm(forms.ModelForm):
    # TeacherUserUpdateForm bilan bog'liq o'zgaruvchilar
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    # TeacherUpdateForm bilan bog'liq o'zgaruvchilar
    mobile = forms.CharField(max_length=13, required=True)

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if models.Teacher.objects.filter(mobile__iexact=mobile).exists():
            self.add_error("mobile", _("Bunday telefon raqam egasi mavjud! Raqamingizni o'zgartiring!"))
        if not mobile:
            raise forms.ValidationError("Telefon raqamingizni kiriting.")
        if len(mobile) < 9 or len(mobile) > 13:
            raise forms.ValidationError("Telefon raqamingiz 9 ta va 13ta raqam oralig'ida bo'lishi kerak!.")
        if not mobile.isdigit():
            raise forms.ValidationError("Telefon raqam faqat sonlardan iborat bo'lishi kerak.")
        return mobile