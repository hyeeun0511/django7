from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    # 규리===========================================
    path('profile_confirm/', views.profile_view, name='profile_confirm'), # 비밀번호 확인 후 마이페이지 이동(251222)
    # 규리===========================================
]
