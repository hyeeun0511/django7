"""
==================== ASGI 설정 ====================
ASGI: Asynchronous Server Gateway Interface
- Django의 비동기 지원을 위한 인터페이스
- WebSocket, 실시간 통신 등 비동기 작업이 필요할 때 사용
- Daphne, Uvicorn 등의 ASGI 서버와 함께 사용
- WSGI는 동기식, ASGI는 비동기식 처리 가능

For more information:
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# ==================== Django 설정 파일 지정 ====================
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mompjt.settings')

# ==================== ASGI 애플리케이션 생성 ====================
# 이 application 객체를 ASGI 서버에 전달하여 비동기 요청 처리
application = get_asgi_application()
