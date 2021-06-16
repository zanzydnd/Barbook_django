release: python3 src/manage.py migrate
web: gunicorn barbook_project.wsgi --log-file --chdir src -