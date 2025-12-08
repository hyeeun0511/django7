from django.urls import path,include
from . import views

app_name=''   # home이기 때문에 -> '' = 아무것도 들어오지않으면
urlpatterns = [
    path('', views.index, name='index'),
]      # home->''
