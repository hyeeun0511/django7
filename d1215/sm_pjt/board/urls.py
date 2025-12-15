from django.urls import path,include
from . import views

app_name = 'board'
urlpatterns = [
    path('list/', views.list, name='list'),
    path('write/', views.write, name='write'),
    path('view/<int:bno>/', views.view, name='view'),   # 링크를 bno로 넘겼으므로 view.py로 가서
    path('delete/<int:bno>/', views.delete, name='delete'),   # 링크를 bno로 넘겼으므로 view.py로 가서
    path('update/<int:bno>/', views.update, name='update'),   # 링크를 bno로 넘겼으므로 view.py로 가서
    path('reply/<int:bno>/', views.reply, name='reply'),   
]
