import pandas as pd
from datetime import datetime
from quiz.models import Result


# Ma'lumotlarni olish
results = Result.objects.all()

# Ma'lumotlarni DataFrame ga o'tkazish
data = []
for result in results:
    data.append({
        'Student': result.student.user.first_name,  # Studentni nomi, ma'lumotlar bazasiga qarang
        'Course': result.course.course_name,    # Kursni nomi, ma'lumotlar bazasiga qarang
        'Marks': result.marks,
        'Question Results': result.question_results,
        'Date': result.date.strftime('%Y-%m-%d %H:%M:%S')
    })

df = pd.DataFrame(data=data)

# Ma'lumotlarni Excel fayliga yozish
excel_filename = 'result_data.xlsx'
df.to_excel(excel_filename, index=False)

print(f"Ma'lumotlar {excel_filename} fayliga yozildi.")