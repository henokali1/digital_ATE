#!/bin/bash
set -e

echo "Activating virtual environment..."
source venv/bin/activate

echo "Pulling latest changes..."
git pull origin master

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Applying migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Restarting Gunicorn..."
sudo systemctl restart digital_ate

echo "Update complete!"
