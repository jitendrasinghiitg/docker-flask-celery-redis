import time
import datetime
import os, traceback
from celery import Celery, states
from celery.exceptions import Ignore

CELERY_BROKER_URL = os.getenv("REDISSERVER", "redis://redisserver:6379")
CELERY_RESULT_BACKEND = os.getenv("REDISSERVER", "redis://redisserver:6379")

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name='hello.task', bind=True)
def hello_world(self, name):
    try:
        if name == 'name':
            k = 1 / 0
        for i in range(60):
            time.sleep(1)
            self.update_state(state='PROGRESS', meta={'done': i, 'total': 60})
        return {"result": "hello {}".format(str(name))}
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise Ignore()
