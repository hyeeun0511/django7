from django.contrib import admin
from student.models import Student

admin.site.register(Student)  
# student>admin.py에 입력시 -> admin사이트에 Student가 표시됨