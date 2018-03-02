#!/usr/bin/env bash

MIGRATION_PATH="./migrations"

if [ "$APP_SETTINGS" = "config.TestingConfig" ]; then
    exec /usr/local/bin/python3.5 /data/manage.py cov
elif [ "$APP_SETTINGS" = "config.ProductionConfig" ]; then

    if [ ! -d "$MIGRATION_PATH" ]; then
        # Python Miration Init
        exec /usr/local/bin/python3.5 /data/manage.py db init
        exec /usr/local/bin/python3.5 /data/manage.py db migrate
    else
        exec /usr/local/bin/python3.5 /data/manage.py db migrate
    fi

    echo -e "Updating Migrations"
    exec /usr/local/bin/python3.5 /data/manage.py db upgrade
    echo -e "DONE"

    chmod 777 /data/
    chmod 777 /data/prod.sqlite

    exec uwsgi --ini ingresse.ini
fi
