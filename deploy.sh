#!/bin/bash
cd /var/www/digital_ate
source venv/bin/activate
git pull origin master
python manage.py collectstatic --noinput
python manage.py migrate
sudo systemctl restart gunicorn
sudo systemctl restart nginx
