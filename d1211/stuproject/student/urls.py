from django.urls import path,include
from . import views

app_name='student'
urlpatterns = [
    path('write/', views.write, name='write'),
    path('list/', views.list, name='list'),
    path('view/<int:sno>/', views.view, name='view'),
    path('delete/<int:sno>/', views.delete, name='delete'),
    path('update/<int:sno>/', views.update, name='update'),
]
# url에서 받으면 requsest에 쓰기
