import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from django.conf import settings


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")





app = Celery("core")
app.conf.enable_utc = True

app.conf.beat_schedule = {

"stock_news": {
    "task": "news.tasks.get_stock_news",
    "schedule": crontab(),
    "args": (settings.SHARE_MARKET_NEWS_API_URL,{"X-RapidAPI-Key": settings.X_RAPID_API_KEY,"X-RapidAPI-Host": settings.X_RAPID_API_HOST},"indian stock"),},



}

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
