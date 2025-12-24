from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('api/kr-admin/', views.kr_admin, name='kr_admin'),
    
    # 게시판 ==========================================혜은
    path('board/', views.board_list, name='board_list'),
    path('board/create/', views.board_create, name='board_create'),   # ✅ 여기로 이동
    path('board/<int:pk>/', views.board_detail, name='board_detail'),
    path('board/<int:pk>/delete/', views.board_delete, name='board_delete'),  # 게시글 삭제 [251224]
    # 게시판 ==========================================혜은
]
