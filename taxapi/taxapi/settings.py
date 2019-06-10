"""
Django settings for taxapi project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import logging
import django.utils.log
import logging.handlers

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^1$b%8zm#)h+bh_s59*60+hdr7=jf&6n)p_a529-9#hwl-f6%a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app.apps.AppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'taxapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'taxapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wjz_information',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
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

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# 创建日志文件夹路径
LOG_PATH = os.path.join(BASE_DIR, 'log')
# 如过地址不存在，则自动创建log文件夹
if not os.path.isdir(LOG_PATH):
    os.mkdir(LOG_PATH)

LOGGING = {
    # 规定只能这样写
    'version': 1,
    # True表示禁用loggers
    'disable_existing_loggers': False,
    # 指定文件写入的格式——这里写了两个不同的格式，方便在后面不同情况需要的时候使用
    'formatters': {
        'default': {
            'format': '%(levelno)s %(funcName)s %(asctime)s %(message)s'
        },
    'standard': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(asctime)s %(message)s'
        }
    },
   'filters': {
       'require_debug_true': {
           '()': 'django.utils.log.RequireDebugTrue',
             },
   },

    'handlers': {
        'all_hanlders': {
            'level': 'DEBUG',
            # 日志文件指定为多大(5M)， 超过大小(5M)重新命名，然后写新的日志文件
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 10 * 1024 * 1024,
            # 储存到的文件地址
            'filename':os.path.join(LOG_PATH, "all.log"),
            'formatter': 'simple',
            'backupCount': 3,
        },
    'file': {
           'level': 'DEBUG',
           'class': 'logging.FileHandler',
           'formatter': 'standard',
           'filename': '%s/all.log' % LOG_PATH, #这是将普通日志写入到日志文件中的方法， 'formatter': 'standard'
    },
   'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout',
   },

    'error': {
        'level': 'ERROR',
        'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
        'filename': '%s/errors.log' % LOG_PATH,  # 日志文件
        'maxBytes': 1024 * 1024 * 8,  # 日志大小 50M
        'backupCount': 3,
        'formatter': 'standard',
    },
  },

'loggers': {
        'django': {
            'handlers': ['file','console'],
            'level': 'DEBUG'
        },
        'errors': {
            'handlers': ['error'],
            'level': 'INFO'
        }

    },

}
