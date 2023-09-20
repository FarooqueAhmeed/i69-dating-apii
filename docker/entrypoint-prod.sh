#!/bin/bash
python3 manage.py runscript fix_old_migration_history
python3 manage.py migrate
python3 manage.py collectstatic --noinput
cp -rf staticfiles/* static/
/usr/local/bin/docker-entrypoint.sh unitd --no-daemon --control unix:/var/run/control.unit.sock
