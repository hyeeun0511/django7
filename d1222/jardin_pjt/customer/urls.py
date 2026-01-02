from django.urls import path,include
from . import views

app_name='customer'
urlpatterns = [
    # html리턴
    path('clist/', views.clist, name='clist'),
    path('cwrite/', views.cwrite, name='cwrite'),
    path('cview/<int:bno>/', views.cview, name='cview'),
    
]

