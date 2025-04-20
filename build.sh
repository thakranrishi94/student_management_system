#!/usr/bin/env bash
pip install -r requirements.txt

# Optional: Apply migrations and collect static files
python manage.py migrate
python manage.py collectstatic --noinput
