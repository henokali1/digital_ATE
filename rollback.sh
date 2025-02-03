#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Please provide a git commit hash to roll back to"
    exit 1
fi

echo "Rolling back to commit $1..."
git checkout $1

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Applying migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Restarting Gunicorn..."
sudo systemctl restart digital_ate

echo "Rollback complete!"
