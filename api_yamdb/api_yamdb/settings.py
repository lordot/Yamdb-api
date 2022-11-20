from datetime import timedelta
import os


RESERVED_NAME = 'me'
MESSAGE_FOR_RESERVED_NAME = 'Имя пользователя "me" использовать нельзя!'
MESSAGE_FOR_USER_NOT_FOUND = 'Пользователя с таким именем нет!'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'



# EMAIL_HOST = 'smtp.email-domain.com'
# EMAIL_HOST_USER = 
# EMAIL_HOST_PASSWORD = 
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# ADMINS = (
#     ('You', 'you@email.com'),
# )
# MANAGERS = ADMINS

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_filters',
    'reviews.apps.ReviewsConfig',
    'api.apps.ApiConfig'
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

ROOT_URLCONF = 'api_yamdb.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'api_yamdb.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static/'),)

# User
AUTH_USER_MODEL = 'reviews.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# token
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
