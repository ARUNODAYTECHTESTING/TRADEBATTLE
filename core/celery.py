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
    "task": "news.tasks.get_news",
    "schedule": crontab(hour=5,minute=0),
    "args": (settings.SHARE_MARKET_NEWS_API_URL,{"X-RapidAPI-Key": settings.X_RAPID_API_KEY,"X-RapidAPI-Host": settings.X_RAPID_API_HOST},"indian stock"),
    },

    "technology_news": {
    "task": "news.tasks.get_news",
    "schedule": crontab(hour=5,minute=0),
    "args": (settings.TECHNOLOGY_URL,{},"technology",{"apiKey":settings.TECHNOLOGY_API_KEY,"country":"in"}),
    },

    "business_news": {
    "task": "news.tasks.get_news",
    "schedule": crontab(hour=5,minute=0),
    "args": (settings.TECHNOLOGY_URL,{},"business",{"apiKey":settings.TECHNOLOGY_API_KEY,"country":"in","category":"business"}),
    },
    "international_news": {
    "task": "news.tasks.get_news",
    "schedule": crontab(hour=5,minute=0),
    "args": (settings.TECHNOLOGY_URL,{},"international",{"apiKey":settings.TECHNOLOGY_API_KEY,"q":"apple","category":"business"}),
    },

    "us stock": {
    "task": "news.tasks.get_news",
    "schedule": crontab(hour=5,minute=0),
    "args": (settings.US_STOCK_URL,{"X-RapidAPI-Key": settings.US_STOCK_X_RAPIDAPI_KEY,"X-RapidAPI-Host": settings.US_STOCK_X_RAPIDAPI_HOST},"us stock",None),
    },

    "india stock": {
    "task": "news.tasks.get_news",
    "schedule": crontab(),
    "args": (settings.INDIA_STOCK_URL,{"X-RapidAPI-Key": settings.INDIA_STOCK_X_RAPIDAPI_KEY,"X-RapidAPI-Host": settings.INDIA_STOCK_X_RAPIDAPI_HOST},"indian stock",{"Indices":"NIFTY 50"}),
    },



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
