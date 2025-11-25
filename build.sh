#!/usr/bin/env bash
# Exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recopilar archivos estáticos
python manage.py collectstatic --no-input

# Crear las tablas en la base de datos
python manage.py migrate

# Cargar los datos iniciales automáticamente
python manage.py loaddata initial_data.json