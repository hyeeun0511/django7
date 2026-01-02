from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ✅ 중복 확인 (AJAX)
    path('check-id/', views.check_id, name='check_id'),
    path('check-nickname/', views.check_nickname, name='check_nickname'),
    path('check-email/', views.check_email, name='check_email'),

    # ✅ 이메일 인증번호 방식 (회원가입 페이지 내부)
    path("email/send-code/", views.send_email_code, name="send_email_code"),
    path("email/verify-code/", views.verify_email_code, name="verify_email_code"),

    # ✅ 아이디/비번 찾기
    path('find-id/', views.find_id, name='find_id'),
    path('find-pw/', views.find_pw, name='find_pw'),

    # ✅ 마이페이지
    path('profile/auth/', views.profile_auth, name='profile_auth'),
    path('profile/', views.profile, name='profile'),
]
