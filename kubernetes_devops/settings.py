"""
Django settings for kubernetes_devops project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import datetime
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')(d0s(5njo15ac6v7!e9ry854rl7rz$zu1+ti)nehzkn&_1w31'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'corsheaders',
    'rest_framework',
    'apps.kubernetes',
    'apps.account',
    'apps.assets',
    'apps.system_logs',
]

CORS_ORIGIN_ALLOW_ALL = True

MIDDLEWARE = [
    #跨域
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]
# 指定ASGI的路由地址
ASGI_APPLICATION = 'kubernetes_devops.routing.application'

# django-channels配置
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

ROOT_URLCONF = 'kubernetes_devops.urls'

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

WSGI_APPLICATION = 'kubernetes_devops.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "kubernetes_devops",
        'HOST': "10.83.8.170",
        "USER": "root",
        # "PASSWORD": "kYw=ha_3reJn5l4",
        "PASSWORD": "tchm8166**!",
        "PORT": "3306",
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# 使用utc时间，前端根据时区自动显示当地时间
USE_TZ = True

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
TEMPLATE_DIRS = (os.path.join(BASE_DIR,  'templates'),)

# 登录URL，验证用户信息使用的model

APPEND_SLASH = False
AUTH_USER_MODEL = 'account.KubernetesSystemUser'
# 接下来是自定义登录字段
# AUTHENTICATION_BACKENDS = (
#     # 是 Django 内置的 Backend
#     'django.contrib.auth.backends.ModelBackend',
# )
REST_FRAMEWORK = {
     'DEFAULT_AUTHENTICATION_CLASSES': (
         # 'rest_framework.authentication.SessionAuthentication',
         # 'rest_framework.authentication.BasicAuthentication',
         # 将token做验证
         # 'rest_framework.authentication.TokenAuthentication',
         'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        ),
    'DEFAULT_PERMISSION_CLASSES': [
            # 'rest_framework.permissions.AllowAny'
            'rest_framework.permissions.IsAuthenticated',
        ]
    }

# jwt载荷中的有效期设置
JWT_AUTH = {
    # token 有效期
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=8),
    # 允许刷新token
    'JWT_ALLOW_REFRESH': True,
     # 续期有效期（该设置可在24小时内带未失效的token 进行续期）
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(hours=24),
    # 自定义返回格式，需要手工创建
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'Component.common.jwt_response.jwt_response_payload_handler',
}

#logging日志配置
log_path = os.path.join(BASE_DIR, "logs")
if not os.path.exists(log_path):
    os.makedirs("logs")

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(os.path.join(BASE_DIR, 'static')),
)

LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'formatters': {
            'standard': {
                'format': '%(asctime)s %(pathname)s process-%(process)d thread-%(thread)d %(lineno)d [%(levelname)s]: %(message)s',
            },
        },
        'handlers': {
            'file_handler': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'logs/app.log',
                'formatter': 'standard'
            },
            # 'console': {
            #     'level': 'DEBUG',
            #     'filters': ['require_debug_true'],
            #     'class': 'logging.StreamHandler',
            #     'formatter': 'standard'
            # },
        },
        'loggers': {
            'django': {
                'handlers': ['file_handler'],
                'propagate': True,
                'level': 'INFO',
                        },
        }
    }

