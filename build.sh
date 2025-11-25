#!/usr/bin/env bash
# Exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recopilar archivos estáticos (CSS, imágenes)
python manage.py collectstatic --no-input

# Aplicar migraciones a la base de datos
python manage.py migrate