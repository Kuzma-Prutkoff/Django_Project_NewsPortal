from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-aj)qx#2l7@ri$nq^e99-$0%%iv)xb^)-kadv+1%$7+52jv@o1z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.sites',

    'news_app',
    'django.contrib.flatpages',
    'django_filters',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',

    "django_apscheduler",
]
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
]

ROOT_URLCONF = 'PortalNews.urls'

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

WSGI_APPLICATION = 'PortalNews.wsgi.application'

# Database https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
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

# Internationalization https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images) https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'

# Default primary key field type https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

LOGIN_REDIRECT_URL = "/post"
LOGOUT_REDIRECT_URL = "/accounts/login"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # встроенный бэкенд Django реализующий аутентификацию по username
    'allauth.account.auth_backends.AuthenticationBackend', # бэкенд аутентификации, предоставленный пакетом allauth
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

ACCOUNT_EMAIL_VERIFICATION = 'mandatory' # верификация включена, чтобы зарегица, нужно пройти по ссылке из письма

ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignupForm"}
#Настройка почты
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # письмо придет на почту
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # письмо придет в консоль
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = "karlusha.zarazniy@yandex.ru"
EMAIL_HOST_PASSWORD = "vzyohuyxqxdxvvti"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = "karlusha.zarazniy@yandex.ru"

#Рассылка менеджерам
SERVER_EMAIL = "karlusha.zarazniy@yandex.ru"
MANAGERS = (
    ('petroffyurchik', 'petroffyurchik@yandex.ru'), # делаем Юрчика менеджером
    ('Petr', 'petr@yandex.ru'), # такого менеджера нет и почты такой нет, но как пример
)
#Рассылка админам
ADMINS = (
    ('petroffyurchik', 'petroffyurchik@yandex.ru'), # и админ и менеджер Юрчик
)

SITE_URL = 'http://127.0.0.1:8000'

APSCHEDULER_DATETIME_FORMAT = 'N j, Y, f:s a'  # формат времени шедулера, специфический такой формат
APSCHEDULER_RUN_NOW_TIMEOUT = 25                # время на выполнение 25 сек иначе выключение процесса

# указывает на URL брокера сообщений (Redis).По умолчанию на порту 6379.
CELERY_BROKER_URL = 'redis://default:qzlMZ2VRlhtk61iac7rlpzsdqJvs9hmb@redis-17053.c61.us-east-1-3.ec2.cloud.redislabs.com:17053'
# указывает на хранилище результатов выполнения задач.
CELERY_RESULT_BACKEND = 'redis://default:qzlMZ2VRlhtk61iac7rlpzsdqJvs9hmb@redis-17053.c61.us-east-1-3.ec2.cloud.redislabs.com:17053'
CELERY_ACCEPT_CONTENT = ['application/json'] # допустимый формат данных.
CELERY_TASK_SERIALIZER = 'json' # метод сериализации задач.
CELERY_RESULT_SERIALIZER = 'json' # метод сериализации результатов.
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_TASK_TIME_LIMIT = 30*60 # время жизни таски

# Кеширование
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'), # Указываем, куда будем сохранять кэшируемые файлы!
        "TIMEOUT": 60,
    }
}

