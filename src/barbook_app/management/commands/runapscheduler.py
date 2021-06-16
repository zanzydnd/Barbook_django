import threading
from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore

# runapscheduler
from barbook_project import settings
from barbook_app.parse import (
    get_ing_tags_and_classes,
    get_cocktails_tags_and_classes,
    get_cocktails,
)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        print("started")

        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # get_ing_tags_and_classes()
        get_cocktails_tags_and_classes()
        get_cocktails()

        try:
            scheduler.start()
        except KeyboardInterrupt as e:
            print(e)
            scheduler.shutdown()
