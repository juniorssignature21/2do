#!/bin/bash

# Build the project...
echo "Building the project..."

# Install dependencies from requirements.txt
pip install setuptools
pip install -r requirements.txt

# Run database migrations (optional, but a good practice)
echo "Make Migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "Collect Static..."
python manage.py collectstatic --noinput

echo "Build process completed!"
