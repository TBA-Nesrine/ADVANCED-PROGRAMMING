"""
Django settings for library_project project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-(_z$1qu14@myu(=j*yme182a7li%6tc*qivm9$*#5)ej*q1*4i'

DEBUG = True
ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'social_django',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
    # Your app
    'library_app',
]

SITE_ID = 1

# Google OAuth2
# Google OAuth2 credentials - Load from config file
try:
    # Try to import from config.py (local file with real credentials)
    from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
    
    # Use the real credentials from config.py
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = GOOGLE_CLIENT_ID
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = GOOGLE_CLIENT_SECRET
    
    print("✓ Using Google OAuth credentials from config.py")
    
except ImportError:
    # If config.py doesn't exist (like on GitHub), use placeholders
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "GOOGLE_CLIENT_ID_PLACEHOLDER"
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "GOOGLE_CLIENT_SECRET_PLACEHOLDER"
    
    print("⚠ Using placeholder Google OAuth credentials")

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'library_app.middleware.RoleBasedRedirectMiddleware',  # ADD THIS HERE
    'allauth.account.middleware.AccountMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'social_core.backends.google.GoogleOAuth2',
)

ROOT_URLCONF = 'library_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'library_project.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
USE_TZ = True


# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Authentication URLs - SET THESE CORRECTLY
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/login/'

# IMPORTANT: Set a default redirect that middleware will override
LOGIN_REDIRECT_URL = '/user/home/'  # Default for regular users

# Social auth redirects - IMPORTANT!
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/user/home/'  # Default
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/user/home/'  # Default for new users

# Allauth settings
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Only define once
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_LOGIN_REDIRECT_URL = '/user/home/'  # Default

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'liliakamiri4@gmail.com'
EMAIL_HOST_PASSWORD = 'jtzf asra jruy fyja'  # For Gmail, use App Password
DEFAULT_FROM_EMAIL = 'liliakamiri4@gmail.com'




# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SITE_URL = "http://127.0.0.1:8000"

# Social auth settings
SOCIAL_AUTH_GOOGLE_OAUTH2_ALLOWED_REDIRECT_URIS = [
    'http://127.0.0.1:8000/oauth/complete/google-oauth2/',
    'http://localhost:8000/oauth/complete/google-oauth2/',
]

SOCIAL_AUTH_PIPELINE = (
    # Get the details from social provider
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    
    # Check if social account already exists
    'social_core.pipeline.social_auth.social_user',
    
    # Get username
    'social_core.pipeline.user.get_username',
    
    # Check if a user with this email already exists
    'social_core.pipeline.user.create_user',
    
    # Associate the social account with the existing user
    'social_core.pipeline.social_auth.associate_user',
    
    # Load extra data
    'social_core.pipeline.social_auth.load_extra_data',
    
    # Update user details
    'social_core.pipeline.user.user_details',
    
    # CUSTOM: Set admin permissions if email matches admin
    'library_app.pipeline.set_admin_permissions',
)

# CRITICAL: This associates by email
SOCIAL_AUTH_ASSOCIATE_BY_EMAIL = True

# Don't create new users if email exists
SOCIAL_AUTH_CREATE_USERS = True

SOCIAL_AUTH_ASSOCIATE_BY_EMAIL = True
SOCIAL_AUTH_LOGIN_ERROR_URL = '/login/error/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False