from django.urls import path,include
from . import views

app_name='event'
urlpatterns = [
    path('write/',views.write,name='write' ),    # 이벤트 등록
]
