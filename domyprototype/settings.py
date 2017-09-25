import os
import sys

PRODUCTION = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))


SECRET_KEY = '71g-ssh03^1&l9o#&nc7yfui73nrh&d5s&l2_e#g%%5vux65!r'

DEBUG = True

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'users',
    'others',
    'statistics',
]

AUTH_USER_MODEL = 'users.UserProfile'

# custom authentication
AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'domyprototype.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'domyprototype.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'domyprototype',
        'USER': 'wxy',
        'PASSWORD': 'Poiu7890',
        'HOST': '60.206.137.157'
    }
}


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


LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False



STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if PRODUCTION == True:
    MEDIA_ROOT = '/usr/share/nginx/html/media'
    STATIC_ROOT = '/usr/share/nginx/html/static'
else:
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )

# email settings

EMAIL_HOST = 'smtp.mxhichina.com'
EMAIL_HOST_USER = 'machine@wangxiyang.com'
EMAIL_HOST_PASSWORD = 'Wxy123456'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_FROM = 'machine@wangxiyang.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'