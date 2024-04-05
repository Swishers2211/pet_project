from celery import shared_task
from masters_guild.celery import app

@app.task
def add(x, y):
    return x + y
