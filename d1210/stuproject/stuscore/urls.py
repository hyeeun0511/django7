from django.urls import path,include
from . import views
app_name='stuscore'
urlpatterns = [
    path('write/', views.write,name="write"),
]