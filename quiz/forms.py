from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from . import models


class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class TeacherSalaryForm(forms.Form):
    salary = forms.IntegerField()


class ClassesForm(forms.Form):
    classes = forms.CharField(max_length=50)


class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['course_name', 'question_number', 'total_marks']


class QuestionForm(forms.ModelForm):

    classes = forms.ModelChoiceField(queryset=models.Classes.objects.all(), empty_label="Sinfni tanlash",
                                     to_field_name="id")

    class Meta:
        model = models.Question
        fields = ['marks', 'question', 'variant_A', 'variant_B', 'variant_C', 'variant_D', 'answer']
        widgets = {
            'question': forms.CharField(widget=CKEditorUploadingWidget()),
            'variant_A': forms.CharField(widget=CKEditorUploadingWidget()),  # Textarea o'lchamini o'zgartirish
            'variant_B': forms.CharField(widget=CKEditorUploadingWidget()),  # Textarea o'lchamini o'zgartirish
            'variant_C': forms.CharField(widget=CKEditorUploadingWidget()),  # Textarea o'lchamini o'zgartirish
            'variant_D': forms.CharField(widget=CKEditorUploadingWidget()),
        }

    def clean(self):
        cleaned_data = super().clean()
        options = [cleaned_data.get('variant_A'), cleaned_data.get('variant_B'), cleaned_data.get('variant_C'), cleaned_data.get('variant_D')]

        if not cleaned_data.get('question') or not cleaned_data.get('marks') or not cleaned_data.get(
                'variant_A') or not cleaned_data.get('variant_B') or not cleaned_data.get(
                'variant_C') or not cleaned_data.get('variant_D') or not cleaned_data.get('answer'):
            raise forms.ValidationError('Barcha maydonlarni to\'ldiring!')
        if len(options) != len(set(options)):
            raise forms.ValidationError('Variantlar bir biriga teng bo\'lishi mumkin emas!')


class UpdateCourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['question_number', 'total_marks', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adding class to the status field to style it as a toggle switch
        self.fields['status'].widget.attrs.update({'class': 'toggle-switch'})
