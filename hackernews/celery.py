import os

from celery import Celery


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "hackernews.settings",
)

app = Celery(
    "hackernews",
)

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)

app.autodiscover_tasks()

from celery.schedules import crontab


app.conf.beat_schedule = {
    "recalculate-trending-posts": {
        "task": "home.tasks.recalculate_trending_posts",
        "schedule": 600.0,  # Every 10 minutes
    },
}