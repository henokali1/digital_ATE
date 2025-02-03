#!/bin/bash
cd /var/www/digital_ate
source venv/bin/activate
python create_inspections.py >> /var/www/digital_ate/logs/cron_inspections.log 2>&1
