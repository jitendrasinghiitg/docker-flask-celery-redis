import time
import os, traceback
from celery import Celery, states

CELERY_BROKER_URL = os.getenv("REDISSERVER", "redis://redisserver:6379")
CELERY_RESULT_BACKEND = os.getenv("REDISSERVER", "redis://redisserver:6379")

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name='hello.task',bind=True)
def hello_world(self, Name):
    try:
        for i in range(60):
            time.sleep(1)
            self.update_state(state='PROGRESS', meta={'done': i, 'total': 60})
        return {"status": "COMPLETED", "result": "hello {}".format(str(Name))}
    except Exception as ex:
        self.update_state(state=states.FAILURE, meta={'custom': '...'})
        return {"status": "FAILURE", "meta":{
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            }}
