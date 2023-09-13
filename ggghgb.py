#
import os
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinequiz.settings')
settings.configure()

# Faylni o'chirish uchun kerakli yo'l
file_to_delete = os.path.join(settings.MEDIA_ROOT, 'media/uploads', '2023-09-11-182659.png')
print(file_to_delete)

# Faylni o'chirish
if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"{file_to_delete} o'chirildi.")
else:
    print(f"{file_to_delete} topilmadi.")


import os
import pandas as pd
from openpyxl import Workbook
from django.conf import settings
#from quiz.models import Result
import django
#
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinequiz.settings')
django.setup()
#
settings.configure()
data = []
latest_date = Result.objects.latest('date').date
results = Result.objects.filter(date=latest_date).select_related('student', 'course', 'classes')
for result in results:
    student = result.student
    data.append({
        'Ism': student.user.first_name,
        'Familiya': student.user.last_name,
        'Kurs': result.course.course_name,
        'Baho': result.marks,
        'Sana': result.date.strftime('%Y-%m-%d %H:%M:%S'),
    })

df = pd.DataFrame(data)
wb = Workbook()
ws = wb.active

for r_idx, row in enumerate(df.iterrows(), start=2):
    for c_idx, value in enumerate(row[1], start=1):
        ws.cell(row=r_idx, column=c_idx, value=value)

wb.save('student_results_latest_date.xlsx')


print('sdsdd')