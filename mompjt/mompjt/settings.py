from pathlib import Path
import os

# ==================== 프로젝트 기본 경로 설정 ====================
BASE_DIR = Path(__file__).resolve().parent.parent  # 프로젝트 루트 디렉토리


# ==================== 보안 설정 ====================
SECRET_KEY = 'django-insecure-j)!mbyhg)gd@vm!+5m2a2xz(s)eso+nnzdx=b4f(3b6g-u(#iz'  # SECRET KEY (운영환경에서는 변경 필수)
DEBUG = True  # 개발 모드 (운영환경에서는 False로 변경)
ALLOWED_HOSTS = []  # 허용할 호스트명 (운영환경에서 설정 필요)


# ==================== Django 앱 등록 ====================
INSTALLED_APPS = [
    # Django 기본 앱
    'django.contrib.admin',         # 관리자 페이지
    'django.contrib.auth',          # 인증 시스템
    'django.contrib.contenttypes',  # 캔텐츠 타입
    'django.contrib.sessions',      # 세션 관리
    'django.contrib.messages',      # 메시지 시스템
    'django.contrib.staticfiles',   # 정적 파일 관리
    'django.contrib.humanize',      # 템플릿 필터 (숫자 포매팅 등)
    
    # 커스터 앱
    'main',        # 메인 페이지
    'accounts',    # 회원 인증
    'map',         # 지도 기능
    'board',       # 게시판 (공지, 자유게시판, 벼룩시장, 댓글)
    'chatbot',     # 챗봇
]

# ==================== 미들웨어 설정 ====================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',         # 보안
    'django.contrib.sessions.middleware.SessionMiddleware',   # 세션
    'django.middleware.common.CommonMiddleware',              # 공통
    'django.middleware.csrf.CsrfViewMiddleware',              # CSRF 보호
    'django.contrib.auth.middleware.AuthenticationMiddleware', # 인증
    'django.contrib.messages.middleware.MessageMiddleware',   # 메시지
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # 클릭재킹 방지
]

ROOT_URLCONF = 'mompjt.urls'  # 메인 URL 설정 파일

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mompjt.wsgi.application'  # WSGI 애플리케이션


# ==================== 데이터베이스 설정 ====================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # SQLite 사용 (개발용)
        'NAME': BASE_DIR / 'db.sqlite3',         # DB 파일 위치
    }
}


# ==================== 비밀번호 검증 규칙 ====================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ==================== 국제화 & 시간대 설정 ====================
LANGUAGE_CODE = 'ko-kr'    # 한국어
TIME_ZONE = 'Asia/Seoul'   # 한국 시간대
USE_I18N = True            # 다국어 지원
USE_TZ = True              # 타임존 인식


# ==================== 정적 파일 (CSS, JS, Image) 설정 ====================
STATIC_URL = 'static/'  # 정적 파일 URL
STATIC_ROOT = BASE_DIR / 'staticfiles'  # collectstatic 결과물 저장 경로 (운영환경)
STATICFILES_DIRS = [    # 프로젝트 루트의 static 폴더 인식
    BASE_DIR / 'static',
]

# ==================== 사용자 업로드 파일 (Media) 설정 ====================
MEDIA_URL = '/media/'           # 미디어 파일 URL
MEDIA_ROOT = BASE_DIR / 'media' # 미디어 파일 저장 경로 (상품 이미지 등)

# ==================== 기본 설정 ====================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # 기본 primary key 타입
AUTH_USER_MODEL = 'accounts.User'  # 커스터 사용자 모델

# # ==================== 이메일 설정 (Gmail SMTP) ====================
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # SMTP 백엔드
# EMAIL_HOST = 'smtp.gmail.com'                                  # Gmail SMTP 서버
# EMAIL_PORT = 587                                               # SMTP 포트
# EMAIL_USE_TLS = True                                           # TLS 암호화
# EMAIL_HOST_USER = 'your-email@gmail.com'                       # 발신 이메일 (수정 필요)
# EMAIL_HOST_PASSWORD = 'your-app-password'                      # Gmail 앱 비밀번호 (수정 필요)
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER                           # 기본 발신자

# ==================== 이메일 설정 (개발용: 콘솔 출력) ====================
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@momslog.local"