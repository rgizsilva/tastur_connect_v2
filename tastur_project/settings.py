# tastur_project/settings.py

import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CONFIGURAÇÕES DE SEGURANça E AMBIENTE ---

# SECRET_KEY: Lê a chave de uma variável de ambiente em produção.
# Se não encontrar, usa uma chave insegura apenas para desenvolvimento local.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-secret-key-here')

# DEBUG: Fica como True localmente, mas será False no Render quando a
# variável de ambiente 'DEBUG' for definida como 'False'.
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS: Configura os domínios permitidos.
# No Render, ele pega o domínio automaticamente. Localmente, permite 'localhost'.
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
else:
    # Para desenvolvimento local, se a variável do Render não existir
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])


# --- APLICAÇÕES E MIDDLEWARE ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # WhiteNoise precisa ser listado aqui, mas geralmente após 'django.contrib.staticfiles'
    'whitenoise.runserver_nostatic', # Adicionado para melhor compatibilidade em desenvolvimento
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'core',
    'clientes',
    'parceiros',
    'reservas',
    'django_select2',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise: Para servir arquivos estáticos em produção de forma eficiente.
    # Deve vir logo após o SecurityMiddleware.
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

# Esta configuração usa a variável de ambiente DATABASE_URL fornecida pelo Render.
# Se ela não existir (localmente), ele usa as credenciais que você já tinha.
DATABASES = {
    'default': dj_database_url.config(
        # Fallback para suas configurações locais se DATABASE_URL não estiver definida
        default='postgres://tastur:tastur123@localhost:5432/tastur',
        conn_max_age=600  # Mantém as conexões abertas por 10 minutos
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


# --- ARQUIVOS ESTÁTICOS (CSS, JavaScript, Imagens) ---
# --- SEÇÃO CORRIGIDA ---

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Esta é a pasta para onde o `collectstatic` irá copiar todos os arquivos.
# O WhiteNoise usará esta pasta para servir os arquivos em produção.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Esta linha ativa o armazenamento otimizado do WhiteNoise.
# É crucial para que ele encontre e sirva os arquivos corretamente.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- CONFIGURAÇÕES ADICIONAIS DO PROJETO ---

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_URL = 'core:login_colaborador'
LOGIN_REDIRECT_URL = 'core:selecao_colaborador'
LOGOUT_REDIRECT_URL = 'core:home'
