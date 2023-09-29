from environs import Env
import os
from pathlib import Path
env = Env()
env.read_env()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.str('DEBUG')


ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # install package
    'drf_yasg',
    'widget_tweaks',
    'ckeditor',
    'django_cleanup',
    'ckeditor_uploader',
    'debug_toolbar',

    # 'quiz',
    'teacher',
    'quiz',
    'student',

]

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_IMAGE_BACKEND = 'pillow'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',

]
ROOT_URLCONF = 'onlinequiz.urls'

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
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },

    }
}

WSGI_APPLICATION = 'onlinequiz.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str("DB_NAME"),
        'HOST': env.str("DB_HOST"),
        'PORT': '5432',
        'USER': env.str("DB_USER"),
        'PASSWORD': env.str("DB_PASSWORD")

    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


MEDIA_ROOT = str(BASE_DIR.joinpath("media"))
MEDIA_URL = '/media/'

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static-files')

LOGIN_REDIRECT_URL = '/afterlogin'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# for contact us give your gmail id and password
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')  # this email will be used to send emails
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL')  # Your email address
ADMIN_EMAIL = env.str('ADMIN_EMAIL')  #


CKEDITOR_RESTRICT_BY_DATE = False


CKEDITOR_CONFIGS = {
  'default': {
      'height': 150,
      'width': 970,
      'removePlugins': 'stylesheetparser',
      'allowedContent': True,
  },
}
CKEDITOR_ALLOW_NONIMAGE_FILES = False


INTERNAL_IPS = [
    '127.0.0.1'
]