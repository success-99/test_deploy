from django import forms
from django.contrib.auth.models import User
from . import models
from quiz import models as QMODEL
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re


class StudentUserForm(forms.ModelForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    con_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'username', 'email']
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
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name.isdigit():  # Faqat sonlardan tashkil topganligini tekshirish
            raise forms.ValidationError("Familyangiz raqamlardan tashkil topishi munkin emas!")
        if len(last_name) < 4:
            raise forms.ValidationError("Iltimos! Familiyangizni 4 ta belgidan kam kiritmang!")
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


class StudentForm(forms.ModelForm):
    classes = forms.ModelChoiceField(queryset=QMODEL.Classes.objects.all(), empty_label="Sinfni tanlash",
                                     to_field_name="id")

    class Meta:
        model = models.Student
        fields = ['mobile']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if models.Student.objects.filter(mobile__iexact=mobile).exists():
            self.add_error("mobile", _("Bunday telefon raqam egasi mavjud! Raqamingizni o'zgartiring!"))
        if not mobile:
            raise forms.ValidationError("Telefon raqamingizni kiriting!")
        if len(mobile) < 9 or len(mobile) > 13:
            raise forms.ValidationError("Telefon raqamingiz 9 ta va 13ta raqam oralig'ida bo'lishi kerak!")
        if not mobile.isdigit():
            raise forms.ValidationError("Telefon raqam faqat sonlardan iborat bo'lishi kerak!")
        return mobile
