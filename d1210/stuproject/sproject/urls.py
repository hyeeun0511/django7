
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/', include('student.urls')),
    path('stuscore/', include('stuscore.urls')),
    path('', include('home.urls')),
]