import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = str(os.getenv('SECRET_KEY'))


DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'backend', 'db', '158.160.77.172']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'users.apps.UsersConfig',
    'api.apps.ApiConfig',
    'recipes.apps.RecipesConfig',
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

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': os.getenv('ENGINE',
                            default='django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', 5432)
    }
}


AUTH_USER_MODEL = "users.User"


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


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PAGINATION_CLASS': [
        'api.pagination.LimitPagination',
    ],
    'PAGE_SIZE': 5,
    'SEARCH_PARAM': 'name',
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'SERIALIZERS': {
        'user_create': 'api.serializers.UserWriteSerializer',
        'user': 'api.serializers.UserListSerializer',
        'current_user': 'api.serializers.UserListSerializer',
        'set_password': 'djoser.serializers.SetPasswordSerializer'
    },
    'HIDE_USERS': False,
    'PERMISSIONS': {
        'user_list': ['rest_framework.permissions.AllowAny'],
        'user': ['djoser.permissions.CurrentUserOrAdminOrReadOnly'],    
        'activation': ['rest_framework.permissions.IsAdminUser'],
        'password_reset': ['rest_framework.permissions.IsAdminUser'],
        'password_reset_confirm': ['rest_framework.permissions.IsAdminUser'],
        'set_password': ['djoser.permissions.CurrentUserOrAdmin'],
        'username_reset': ['rest_framework.permissions.IsAdminUser'],
        'username_reset_confirm': ['rest_framework.permissions.IsAdminUser']
    }
}

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)


STATIC_URL = '/static/backend_static/'
STATIC_ROOT = '/static/backend_static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Registration user model settings
EXCEPTION_CHARACTERS = r'[^\w.@+-]'
NAME_LENGHT = 150
MIN_USERNAME = 3
MAX_USERNAME = 24
EMAIL_LENGHT = 254
COLOR_LENGHT = 7
UNIT_LENGHT = 24
TEXT_LENGHT = 3000
MIN_AMOUNT = 1
MAX_AMOUNT = 32000
# Download shopping_list
FILE_NAME = 'shopping_cart.txt'
