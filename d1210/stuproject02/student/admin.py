from django.contrib import admin
from student.models import Student
# from .models import Student    -> student 생략 가능

# admin사이트에 Student를 등록해달라는 의미  - 등록은 되지만 db가 없을시 에러남 
admin.site.register(Student)
