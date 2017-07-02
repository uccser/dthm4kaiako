release: python cs4teachers/manage.py migrate
web: gunicorn --pythonpath cs4teachers config.wsgi --log-file=-
