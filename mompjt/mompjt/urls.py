# ==================== URL 설정 ====================
# 프로젝트의 모든 URL을 관리하는 메인 파일
# 각 앱의 urls.py를 include()로 연결

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 관리자 페이지
    path('admin/', admin.site.urls),
    
    # 메인 페이지 (/ )
    path('', include(('main.urls', 'main'))),
    
    # 회원 인증 (/accounts/ )
    # - 회원가입, 로그인, 로그아웃, 프로필, 비밀번호 변경 등
    path('accounts/', include('accounts.urls')),
    
    # 지도 기능 (/map/ )
    path('map/', include('map.urls')),
    
    # 게시판 (/board/ )
    # - 공지사항, 자유게시판, 벼룩시장(찜, 댓글 등)
    path('board/', include('board.urls')),
    
    # 챗봇 (/chatbot/ )
    path('chatbot/', include('chatbot.urls'))
]

# ==================== 미디어 파일 서빙 (개발환경) ====================
# DEBUG=True 일 때만 미디어 파일을 직접 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
