from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


from .models import User


@admin.register(User)
class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'password',
        'is_active',
     
    )
    list_filter = ('is_active', )


{"curriculum": "thai",
 "questionType": "MCQ",
 "question": [{"type": "text",
   "value": "กำหนดให้ \\(0^{\\circ}<{A}<90^{\\circ}\\) แล้วมุม \\({A}\\) จากสมการ \\(\\sin {A} \\cos {A}-\\dfrac{\\sqrt{2}}{2} \\sin {A}-\\dfrac{1}{2} \\cos {A}+\\dfrac{\\sqrt{2}}{4}=0\\)  มีค่าตรงกับข้อใดต่อไปนี้"}],
 "choices": [[{"type": "text", "value": "\\(30^{\\circ}\\)"},
   {"type": "answer", "value": True}],
  [{"type": "text", "value": "\\(45^{\\circ}\\)"},
   {"type": "answer", "value": False}],
  [{"type": "text", "value": "\\(60^{\\circ}\\)"},
   {"type": "answer", "value": False}],
  [{"type": "text", "value": "ถูกทั้งข้อ \\(1\\) และ \\(2\\)"},
   {"type": "answer", "value": False}]],
 "numberOfChoices": 4,
 "keyChoice": "\\(30^{\\circ}\\)",
 "subject": "คณิตศาสตร์",
 "author": "3m5WfugQlsNp8levq8uybh6b3G43",
 "exam": "สอบเข้า รร.เตรียมทหาร",
 "level": "มัธยม 3",
 "examBoard": "",
 "papaerCode": "",
 "hardness": "62",
 "topics": ["อัตราส่วนตรีโกณมิติ"],
 "isDraft": False,
 "isVerified": True,
 "number": "2151",
 "similarityText": "กำหนดให้ \\(0^{\\circ}<{A}<90^{\\circ}\\) แล้วมุม \\({A}\\) จากสมการ \\(\\sin {A} \\cos {A}-\\dfrac{\\sqrt{2}}{2} \\sin {A}-\\dfrac{1}{2} \\cos {A}+\\dfrac{\\sqrt{2}}{4}=0\\)  มีค่าตรงกับข้อใดต่อไปนี้^||$\\(30^{\\circ}\\) #||# \\(45^{\\circ}\\) #||# \\(60^{\\circ}\\) #||# ถูกทั้งข้อ \\(1\\) และ \\(2\\)"}