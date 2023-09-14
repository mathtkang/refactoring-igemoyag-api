from pathlib import Path
import os
import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, True))

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")

ALLOWED_HOSTS = [
    # "*",
    'backend-api',
    '127.0.0.1',
    '172.31.39.243',
]

# Application definition
SYSTEM_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    # [Django-Rest-Framework]
    "rest_framework",
    "rest_framework.authtoken",  # admin 페이지에서 새로운 모델이 보여짐 / 이걸 해야 drf의 jwt기능 사용 가능
    "corsheaders",  # CORS
    "drf_yasg",  # swagger
]

CUSTOM_APPS = [
    "accounts.apps.AccountsConfig",
    "auths.apps.AuthsConfig",
    "common.apps.CommonConfig",
    "pills.apps.PillsConfig",
    "users.apps.UsersConfig",
]

INSTALLED_APPS = SYSTEM_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS 미들웨어 추가
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        "rest_framework.authentication.SessionAuthentication",   # default authentication
        "rest_framework.authentication.TokenAuthentication",
        "config.authentication.JWTAuthentication",
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

ROOT_URLCONF = 'config.root_urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
POSTGRESQL_DB = env('POSTGRESQL_DB')
if POSTGRESQL_DB:
    DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql",
        'NAME': env("DB_NAME"),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"),
        'PORT': env("DB_PORT"),
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Password validation
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

# Internationalization
LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"  # 데이터 베이스 시간대 설정시 문자열로

USE_I18N = True  # 장고 번역 시스템 활성화 여부

USE_TZ = False  # True(디폴트)인 경우 미국 시간 사용. False 로 변경해 주어야 설정한 시간대로 변경됨. (한국에서만 운영할 사이트, db에서 날짜와 시간을 헷갈리지 않게 하기 위해서)

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Customizing User model
AUTH_USER_MODEL = "users.User"
# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',  # 필수
#     # 'allauth.account.auth_backends.AuthenticationBackend',  # allauth 사용 시 필수
# ]
# SITE_ID = 1  # allauth 사용 시 필수

PHOTO_KEY = env("PHOTO_KEY")


# [SEND to Email Message]
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"  # 메일을 보내는 호스트 서버
EMAIL_PORT = 587  # ENAIL_HOST에 정의된 SMTP 서버가 사용하는 포트 (587: TLS/STARTTLS용 포트)
EMAIL_HOST_USER = env("EMAIL_HOST_USER")  # 발신할 이메일 주소
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")  # 발신할 이메일 비밀번호 (2단계 인증일 경우 앱 비밀번호 16자리)
EMAIL_USE_TLS = True  # TLS 보안 방법 (SMPT 서버와 통신할 떄 TLS (secure) connection 을 사용할지 말지 여부)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # 사이트와 관련한 자동응답을 받을 이메일 주소


# CORS settings: 보안 설정은 상황에 따라 조절
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_WHITELIST = ['http://43.202.87.58']

# CSRF settings: CSRF 허용 목록을 CORS와 동일하게 설정합니다.
CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST
