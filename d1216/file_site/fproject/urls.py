from django.contrib import admin
from django.urls import path,include
from django.conf import settings # 파일 업로드 시 추가
from django.conf.urls.static import static # 파일 업로드 시 추가

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('board/', include('board.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # 파일 업로드 시 추가
