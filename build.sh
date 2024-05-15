#!/usr/bin/env bash
# exit on error
# test one 
set -o errexit

poetry install

python manage.py collectstatic --no-input
python manage.py migrate
