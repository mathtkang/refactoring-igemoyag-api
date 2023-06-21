"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import environ


env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY SOCIAL CLIENT KEY
# KAKAO_REST_API_KEY = env("KAKAO_REST_API_KEY")
# GOOGLE_CLIENT_ID = env("GOOGLE_CLIENT_ID")
# GOOGLE_SECRET = env("GOOGLE_SECRET")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = "RENDER" not in os.environ

ALLOWED_HOSTS = ["*"]


# Application definition

SYSTEM_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

CUSTOM_APPS = [
    "auths.apps.AuthsConfig",
    "common.apps.CommonConfig",
    "pills.apps.PillsConfig",
    "users.apps.UsersConfig",
]

THIRD_PARTY_APPS = [
    # [Django-Rest-Framework]
    "rest_framework",
    "rest_framework.authtoken",  # admin 페이지에서 새로운 모델이 보여짐
    # "corsheaders",  # CORS
    "drf_yasg",  # swagger
]

INSTALLED_APPS = SYSTEM_APPS + CUSTOM_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "refactoring",  # DB name
        "USER": "igmy",  # User name in postgresql
        "PASSWORD": "devpassword",
        # "HOST": "elice-kdt-2nd-team6.koreacentral.cloudapp.azure.com",
        "HOST": "127.0.0.1",
        "PORT": 5432,
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        "rest_framework.authentication.SessionAuthentication",   # default authentication
        "rest_framework.authentication.TokenAuthentication",
        "config.authentication.JWTAuthentication",
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"  # 데이터 베이스 시간대 설정시 문자열로

USE_I18N = True  # 장고 번역 시스템 활성화 여부

# USE_L10N = True  # 현지화 데이터 형식 사용 여부

USE_TZ = False  # True(디폴트)인 경우 미국 시간 사용. False 로 변경해 주어야 설정한 시간대로 변경됨. (한국에서만 운영할 사이트, db에서 날짜와 시간을 헷갈리지 않게 하기 위해서)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Customizing User model
AUTH_USER_MODEL = "users.User"  # <myapp_name>.<user_model_name>


# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',  # 필수
#     # 'allauth.account.auth_backends.AuthenticationBackend',  # allauth 사용 시 필수
# ]

# # SITE_ID = 1  # allauth 사용 시 필수