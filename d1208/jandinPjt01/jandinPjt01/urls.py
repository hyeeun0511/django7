from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('event/', include('event.urls')),
    path('', include('home.urls')),  # 링크뒤에 아무것도 붙지않으면 home으로 오라는 의미
]
