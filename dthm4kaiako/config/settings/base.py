"""
Base Django settings for DTHM for Kaiako project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os.path
import environ


# dthm4kaiako/dthm4kaiako/config/settings/base.py - 3 = dthm4kaiako/dthm4kaiako/
ROOT_DIR = environ.Path(__file__) - 3

env = environ.Env()

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)

# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = 'Pacific/Auckland'
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-NZ'
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = False
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

DATE_FORMAT = 'j M Y'                   # '25 Oct 2006'
TIME_FORMAT = 'P'                       # '2:30 p.m.'
DATETIME_FORMAT = 'j M Y, P'            # '25 Oct 2006, 2:30 p.m.'
YEAR_MONTH_FORMAT = 'F Y'               # 'October 2006'
MONTH_DAY_FORMAT = 'j F'                # '25 October'
SHORT_DATE_FORMAT = 'd/m/Y'             # '25/10/2006'
SHORT_DATETIME_FORMAT = 'd/m/Y P'       # '25/10/2006 2:30 p.m.'
FIRST_DAY_OF_WEEK = 0                   # Sunday

# The *_INPUT_FORMATS strings use the Python strftime format syntax,
# see https://docs.python.org/library/datetime.html#strftime-strptime-behavior
DATE_INPUT_FORMATS = [
    '%d/%m/%Y', '%d/%m/%y',             # '25/10/2006', '25/10/06'
    # '%b %d %Y', '%b %d, %Y',          # 'Oct 25 2006', 'Oct 25, 2006'
    # '%d %b %Y', '%d %b, %Y',          # '25 Oct 2006', '25 Oct, 2006'
    # '%B %d %Y', '%B %d, %Y',          # 'October 25 2006', 'October 25, 2006'
    # '%d %B %Y', '%d %B, %Y',          # '25 October 2006', '25 October, 2006'
]
DATETIME_INPUT_FORMATS = [
    '%Y-%m-%d %H:%M:%S',                # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',             # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',                   # '2006-10-25 14:30'
    '%Y-%m-%d',                         # '2006-10-25'
    '%d/%m/%Y %H:%M:%S',                # '25/10/2006 14:30:59'
    '%d/%m/%Y %H:%M:%S.%f',             # '25/10/2006 14:30:59.000200'
    '%d/%m/%Y %H:%M',                   # '25/10/2006 14:30'
    '%d/%m/%Y',                         # '25/10/2006'
    '%d/%m/%y %H:%M:%S',                # '25/10/06 14:30:59'
    '%d/%m/%y %H:%M:%S.%f',             # '25/10/06 14:30:59.000200'
    '%d/%m/%y %H:%M',                   # '25/10/06 14:30'
    '%d/%m/%y',                         # '25/10/06'
]
DECIMAL_SEPARATOR = '.'
THOUSAND_SEPARATOR = ','
NUMBER_GROUPING = 3


# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres:///dthm4kaiako'),
}
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
DATABASES['default']['ATOMIC_REQUESTS'] = True

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'config.urls'
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'filebrowser',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    # Handy template tags
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.gis',
    # Full text search
    'django.contrib.postgres',
    # Include forms application as default renderer is overwritten
    'django.forms',
]
THIRD_PARTY_APPS = [
    'corsheaders',
    'anymail',
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',
    'markdownx',
    'mapwidgets',
    'captcha',
    'django_filters',
    'modelclone',
    'svg',
    'tinymce',
]
LOCAL_APPS = [
    'general.apps.GeneralAppConfig',
    'users.apps.UsersAppConfig',
    'get_started.apps.GetStartedAppConfig',
    'resources.apps.ResourcesAppConfig',
    'events.apps.EventsAppConfig',
    'dtta.apps.DttaAppConfig',
    'learning_area_cards.apps.LearningAreaCardsAppConfig',
    'poet.apps.POETAppConfig',
    'secret_pages.apps.SecretPagesAppConfig',
    'ara_ako.apps.AraAkoAppConfig',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {
    'sites': 'contrib.sites.migrations'
}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'users.User'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = 'users:redirect'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = 'account_login'

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
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

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    'allauth.account.middleware.AccountMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = os.path.join(str(ROOT_DIR.path('staticfiles')), '')

# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
BUILD_ROOT = os.path.join(str(ROOT_DIR.path('build')), '')
STATICFILES_DIRS = [
    BUILD_ROOT,
]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = os.path.join(str(ROOT_DIR.path('media')), '')
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'


# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(ROOT_DIR.path('templates')),
        ],
        'OPTIONS': {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'config.context_processors.api_keys.api_keys',
                'config.context_processors.deployed.deployed',
                'config.context_processors.dtta_menu.dtta_menu',
                'config.context_processors.version_number.version_number',
            ],
            'libraries': {
                'markdown': 'config.filters.markdown',
                'get_item': 'config.filters.get_item',
                'query_replace': 'config.templatetags.query_replace',
                'poet_templatetags': 'poet.templatetags',
                'read_static_file': 'config.templatetags.read_static_file',
            },
        },
    },
]

# FORMS
# ------------------------------------------------------------------------------
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'
CRISPY_TEMPLATE_PACK = 'bootstrap4'


# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (
    str(ROOT_DIR.path('fixtures')),
)


# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = 'DENY'


# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')


# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = 'admin/'
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ('UCCSER', 'csse-education-research@canterbury.ac.nz'),
]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS


# django-allauth
# ------------------------------------------------------------------------------
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ALLOW_REGISTRATION = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_SIGNUP_FORM_CLASS = 'users.forms.SignupForm'
ACCOUNT_ADAPTER = 'users.adapters.AccountAdapter'
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_ADAPTER = 'users.adapters.SocialAccountAdapter'


# tinymce (for uploading images in news postings)
# ------------------------------------------------------------------------------
TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 500,
    "menubar": False,
    "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
    "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,"
    "code,help,wordcount",
    "toolbar": "undo redo | formatselect | "
    "bold italic backcolor | alignleft aligncenter "
    "alignright alignjustify | bullist numlist outdent indent | "
    "removeformat | image | help",
}

TINYMCE_FILEBROWSER = True

FILEBROWSER_DIRECTORY = 'text-editor/'

FILEBROWSER_SELECT_FORMATS = {
    'file': ['Image'],
    'image': ['Image']
}

FILEBROWSER_EXTENSIONS = {
    'Image': ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']
}

# django-rest-framework
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10
}

# LOGGING
# ------------------------------------------------------------------------------
# Based off https://lincolnloop.com/blog/django-logging-right-way/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "%(asctime)s %(levelname)-6s %(lineno)-4s%(name)-15s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        # Root logger
        "": {
            "level": env("LOG_LEVEL", default="INFO"),
            "handlers": ["console", ],
        },
        "django": {
            "level": env("LOG_LEVEL", default="INFO"),
            "handlers": ["console", ],
            "propagate": False,
        },
        'gunicorn.error': {
            "level": env("LOG_LEVEL", default="INFO"),
            'handlers': ['console', ],
            'propagate': False,
        },
        'gunicorn.access': {
            "level": env("LOG_LEVEL", default="INFO"),
            'handlers': ['console', ],
            'propagate': False,
        },
    },
}

# MAPS (django-map-widgets)
# ------------------------------------------------------------------------------
MAP_WIDGETS = {
    "GooglePointFieldWidget": (
        ("zoom", 5),
        ('mapCenterLocation', [-41, 174]),
        ("GooglePlaceAutocompleteOptions",
            {'componentRestrictions': {'country': 'nz'}}),
        ("markerFitZoom", 12),
    ),
}


# Learning Area Cards
# ------------------------------------------------------------------------------
LEARNING_AREA_CARDS_GENERATION_LOCATION = os.path.join(
    str(ROOT_DIR.path("staticfiles")),
    "learning_area_cards"
)
LEARNING_AREA_CARDS_FILENAME_TEMPLATE = 'Learning Area Cards - {card_set_title} - {print_type} sided.pdf'
LEARNING_AREA_CARDS_SINGLE_PRINT = 'Single'
LEARNING_AREA_CARDS_DOUBLE_PRINT = 'Double'
LEARNING_AREA_CARDS_PRINT_TYPES = (LEARNING_AREA_CARDS_SINGLE_PRINT, LEARNING_AREA_CARDS_DOUBLE_PRINT)


# Other
# ------------------------------------------------------------------------------
DEPLOYED = env.bool("DEPLOYED")
GIT_SHA = env("GIT_SHA", default=None)
if not GIT_SHA:
    GIT_SHA = "local development"
PRODUCTION_ENVIRONMENT = False
STAGING_ENVIRONMENT = False
SAMPLE_DATA_ADMIN_PASSWORD = env('SAMPLE_DATA_ADMIN_PASSWORD', default='password')
SAMPLE_DATA_USER_PASSWORD = env('SAMPLE_DATA_USER_PASSWORD', default='password')
SECRET_PAGES_TEMPLATE_TEMPLATE = 'secret_pages/{}.html'
SVG_DIRS = [os.path.join(str(ROOT_DIR.path("staticfiles")), "svg")]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
X_FRAME_OPTIONS = "SAMEORIGIN"
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://canterbury.ac.nz"
]
CSRF_TRUSTED_ORIGINS = [
    'https://dthm4kaiako-dev.csse.canterbury.ac.nz',
    'https://dthm4kaiako.ac.nz',
]
