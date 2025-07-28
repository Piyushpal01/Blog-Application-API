#!/usr/bin/env bash

set -o errexit  # exit on error

cd blog_app

pip install -r requirements.txt

python manage.py collectstatic --no-input   # Django ki ek built-in command hai jo saare static files ko ek central location (usually static/ folder) mein collect kar deti hai.
python manage.py migrate