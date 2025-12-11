from django.db import models


# models에 있는 Model class를 만들겠다는것
# 파이썬구문으로
# 테이블을 생성하면 항상 id - AutoField로 생성이 됨
# 테이블명 student_student                         (student라는 앱의 student라는 테이블이 만들어졌다는 뜻)
class Student(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=1)
    grade = models.IntegerField(default=1)
    gender = models.CharField(max_length=10)
    hobby = models.CharField(max_length=100,default='게임') # 아무것도 넣지않으면 게임
    
    def __str__(self):
        return f"{self.sno},{self.name},{self.age},{self.grade},{self.gender}"         # django사이트 -> student 리스트에 작성되는 내용
# student라는 객체를 찍으면 밑에 함수가 나옴