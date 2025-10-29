#!/usr/bin/env bash
# exit on error
set -o errexit

# Instala as dependências
pip install -r requirements.txt

# Coleta os arquivos estáticos (CSS, JS, etc.)
python manage.py collectstatic --no-input

# Aplica as migrações do banco de dados
python manage.py migrate

# Cria o superusuário usando nosso comando personalizado
python manage.py create_superuser
