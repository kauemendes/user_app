#!/usr/bin/env bash

MIGRATION_PATH="./migrations"

if [ ! -d "$MIGRATION_PATH" ]; then
    # Python Miration Init
    /usr/local/bin/python3.5 /data/manage.py db init
    /usr/local/bin/python3.5 /data/manage.py db migrate
else
    /usr/local/bin/python3.5 manage.py db migrate
fi

echo -e "Updating Migrations"
python manage.py db upgrade
echo -e "DONE"

uwsgi --ini ingresse.ini