from django.urls import path,include
from . import views

app_name = 'product'
urlpatterns = [
    path('detail/', views.detail, name='detail'),  # 상품 상세페이지
    # 카카오 결제요청
    path('prepare_payment/', views.prepare_payment, name='prepare_payment'),  # 결제 준비단계
    
    path('approve/', views.approve, name='approve'),  # 결제 승인페이지
    # 카카오결제후 이동
    path('success/', views.success, name='success'),  # 결제 성공페이지
    path('fail/', views.fail, name='fail'),           # 결제 실패페이지
    path('cancel/', views.cancel, name='cancel'),     # 결제 취소페이지
]

