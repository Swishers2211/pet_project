import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'masters_guild.settings')

REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

app = Celery('masters_guild')
app.conf.update(broker_url=f"redis://:{REDIS_PASSWORD}@redis:6379/0", result_backend=f"redis://:{REDIS_PASSWORD}@redis:6379/0")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
