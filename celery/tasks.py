import time
import os
from celery import Celery

CELERY_BROKER_URL = os.getenv("REDISSERVER", "redis://redisserver:6379")
CELERY_RESULT_BACKEND = os.getenv("REDISSERVER", "redis://redisserver:6379")

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name='hello.task')
def hello_world(Name):
    try:
        time.sleep(60)
        return {"status": "COMPLETED", "result": "hello {}".format(str(Name))}
    except:
        return
