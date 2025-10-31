# tastur_project/settings.py

import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CONFIGURAÇÕES DE SEGURANÇA E AMBIENTE ---

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-secret-key-here')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
else:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1', '8000-i0r2kgzpz4wncs0ggucup-3029f0f6.manusvm.computer'])


# --- APLICAÇÕES E MIDDLEWARE ---

INSTALLED_APPS = [
    # Apps do Django devem vir primeiro
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # WhiteNoise para servir estáticos
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    
    # Apps de terceiros
    'crispy_forms',
    'crispy_bootstrap5',
    'rest_framework',
    'django_select2',

    # Seus apps
    'core',
    'clientes',
    'parceiros',
    'reservas',
    'analise',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise Middleware deve vir logo após o SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tastur_project.urls'

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

WSGI_APPLICATION = 'tastur_project.wsgi.application'


# --- BANCO DE DADOS ---

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://tastur:tastur123@localhost:5432/tastur',
        conn_max_age=600
    )
}



# --- VALIDAÇÃO DE SENHAS ---

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- INTERNACIONALIZAÇÃO ---

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# --- ARQUIVOS ESTÁTICOS (CONFIGURAÇÃO FINAL E ROBUSTA) ---

STATIC_URL = '/static/'
# Diretório onde o `collectstatic` irá copiar todos os arquivos para produção.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Diretórios extras onde o Django deve procurar por arquivos estáticos.
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Mecanismo de armazenamento do WhiteNoise. Essencial para produção.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- CONFIGURAÇÕES ADICIONAIS DO PROJETO ---

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_URL = 'core:login_colaborador'
LOGIN_REDIRECT_URL = 'core:selecao_colaborador'
LOGOUT_REDIRECT_URL = 'core:home'

