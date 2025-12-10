from django.db import models

class Student(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=1)
    grade = models.IntegerField(default=1)
    gender = models.CharField(max_length=10)
    hobby = models.CharField(max_length=100,default='게임') # 아무것도 넣지않으면 게임
    
    def __str__(self):
        return f"{self.sno},{self.name},{self.age},{self.grade},{self.gender},{self.hobby}"         # django사이트 -> student 리스트에 작성되는 내용
# student라는 객체를 찍으면 밑에 함수가 나옴