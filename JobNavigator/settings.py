# settings.py
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
# Language settings
LANGUAGE_CODE = 'en-us'  # This specifies the language code (English - US)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'core',
      # Replace with your actual app name
]

# Secret Key configuration
SECRET_KEY = 'LrQdHRHjIvhC8KN_1114rbux0StKki9d1h3ve8mBlrzROUe5hV16o5PJb0Qg1WRQ-WQ'  # Replace with your generated key

# Database configuration to connect to SQL Server using `django-mssql-backend`
DATABASES = {
    'default': {
        'ENGINE': 'mssql',  # This is the correct engine for SQL Server
        'NAME': 'JobNavigatorDB',  # Your database name
        'USER': '',  # Leave empty for Windows Authentication (if you're using it)
        'PASSWORD': '',  # Leave empty for Windows Authentication (if you're using it)
        'HOST': 'LAPTOP-PS334HAN',  # The host where your SQL Server is running (e.g., 'localhost' or your server name)
        'PORT': '1433',  # Leave empty to use the default SQL Server port (1433)
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',  # Ensure this driver is installed
            'trusted_connection': 'yes',
              'timeout': 30,  # This enables Windows Authentication
        },
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core' / 'templates',
 ],  # Add this line
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.static',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# MIDDLEWARE setting in settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Must be before AuthenticationMiddleware
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'core.auth_backend.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',  # Default Django authentication
]

ROOT_URLCONF = 'JobNavigator.urls'


# Email settings for sending notifications (using Gmail as an example)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'projectforlec00@gmail.com'
EMAIL_HOST_PASSWORD = 'baue khmo wecv uvkj'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


#Error Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'error.log',  # Error logs saved here
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

LOGIN_URL = "login" 
# LOGIN_URL = '/jobseeker/profile/'
LOGOUT_REDIRECT_URL = 'home'
 
# Allowed hosts configuration
ALLOWED_HOSTS = ['localhost', '127.0.0.1'] #'LAPTOP-PS334HAN', '192.168.1.85']  # Adjust based on your environment

# Ensure you have debug mode set as needed
DEBUG = True # Set to False in production

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,"core/static"),  # Dynamically sets the path to the static folder
]

STATIC_ROOT = BASE_DIR / 'staticfiles'  # Adjust the path if needed

# Media files (Uploaded by users)
MEDIA_URL = '/media/'  # URL for accessing media files
MEDIA_ROOT = BASE_DIR / "media"  # Directory to save uploaded files


# CSRF_COOKIE_SECURE = False  # Should be False in development
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000']  # Add your domain

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "x-csrftoken",
]

CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_SECURE = True  # Set to True if using HTTPS


# Other necessary settings (optional)

# You can add additional configurations here based on your project needs
SESSION_ENGINE = "django.contrib.sessions.backends.db"  # Store sessions in DB
SESSION_COOKIE_AGE = 1209600  # Keep session for 2 weeks
SESSION_SAVE_EVERY_REQUEST = True  # Save session on every request
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Keep user logged in even after closing browser
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_SECURE = False