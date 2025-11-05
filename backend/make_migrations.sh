#!/bin/bash
# Script to create migrations for all apps

echo "Creating migrations for all apps..."

python manage.py makemigrations accounts
python manage.py makemigrations forms
python manage.py makemigrations submissions
python manage.py makemigrations analytics
python manage.py makemigrations webhooks

echo "Migrations created! Run 'python manage.py migrate' to apply them."

