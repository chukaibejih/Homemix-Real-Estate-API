#!/usr/bin/env bash
# exit on error
set -o errexit

pipenv install

python manage.py collectstatic --no-input
python manage.py migrate