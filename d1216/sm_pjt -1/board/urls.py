from django.urls import path,include
from . import views

app_name='board'
urlpatterns = [
    path('list/', views.list, name='list'),
    path('write/', views.write, name='write'),
    path('view/<int:bno>/', views.view, name='view'),
    path('delete/<int:bno>/', views.delete, name='delete'),
    path('update/<int:bno>/', views.update, name='update'),
    path('reply/<int:bno>/', views.reply, name='reply'),
]
