#!/bin/bash

echo "Compiling message files"
/docker_venv/bin/python3 ./manage.py compilemessages

ls
ls ./dthm4kaiako/

# Start gunicorn service
echo "Starting gunicorn"
/docker_venv/bin/gunicorn -c gunicorn.conf.py -b :8080 config.wsgi
