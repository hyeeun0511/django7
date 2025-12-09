from django.urls import path,include
from . import views

app_name='community'
urlpatterns = [
    path('write/', views.write, name='write'),
]
