import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barbook_project.settings")

app = Celery("barbook_project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(packages=["barbook_app"])
