from django.urls import path,include
from . import views

app_name = ''   # app_name이 아무이름 없이 들어옴
urlpatterns = [
    path('',views.index,name='index'),  # 링크뒤에 아무것도 붙지않으면 home으로 오라는 의미
]    # url에 아무것도 들어오지않으면 views.index 실행
