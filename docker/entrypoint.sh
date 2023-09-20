#!/bin/bash
python3 manage.py runscript fix_old_migration_history
python3 manage.py migrate
python3 manage.py collectstatic --noinput
exec /usr/bin/supervisord