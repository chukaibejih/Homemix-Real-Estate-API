#!/usr/bin/env bash
# exit on error
set -o errexit

pipenv install --upgrade pipenv

python manage.py collectstatic --no-input
python manage.py migrate