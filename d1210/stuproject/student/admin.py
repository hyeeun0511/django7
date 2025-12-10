from django.contrib import admin
from student.models import Student
# from .models import Student    -> student 생략 가능

# admin사이트에 Student를 등록해달라는 의미  - 등록은 되지만 db가 없을시 에러남 
admin.site.register(Student)

# python manage.py makemigrations   -> terminal에 작성 시 sql형태에 맞게 변경됨
# python manage.py migrate          -> terminal 작성
# python manage.py showmigrations   -> migration한게 뭐있는지 보여줌  :rollback시켜서 데이터 변경가능
# 사이트에섯 student 추가
#--
# python manage.py migrate student 0001_initial
# python manage.py migrate admin 0001_initial
# python manage.py migrate  :기존의것 모두 생성
#--