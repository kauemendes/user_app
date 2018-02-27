#!/usr/bin/env bash

MIGRATION_PATH="./migrations"

if [ ! -d "$MIGRATION_PATH" ]; then
    # Python Miration Init
    /usr/local/bin/python3.5 /data/manage.py db init
    rm -rf /data/migrations/env.py
    cp /data/env.py /data/migrations/
    /usr/local/bin/python3.5 /data/manage.py db migrate
else
    rm -rf /data/migrations/env.py
    cp env.py /data/migrations/
    /usr/local/bin/python3.5 manage.py db migrate
fi

echo -e "Updating Migrations"
python manage.py db upgrade
echo -e "DONE"

uwsgi --ini ingresse.ini