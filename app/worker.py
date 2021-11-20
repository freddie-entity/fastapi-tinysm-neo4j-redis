import os
from celery import Celery
from time import sleep

from config import settings


celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND


@celery.task(name='reverse')
def reverse(text):
    sleep(5)
    return text[::-1]

