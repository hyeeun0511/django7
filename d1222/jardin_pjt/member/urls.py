from django.urls import path,include
from . import views

app_name = 'member'
urlpatterns = [
    # html 리턴
    path('step03/', views.step03, name='step03'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    # JSON 리턴 : ID가 존재하는지 체크하는 JSON응답 처리
    path('idCheck/', views.idCheck, name='idCheck'),
]

