import json
import celery.states as states
from flask import Flask, request, jsonify, url_for
from worker import celery

app = Flask(__name__)


@app.route('/')
def welcome():
    return 'flask-celery-redis-demo'


@app.route("/hello_world", methods=['POST'])
def predict():
    input1 = request.get_json()
    name = input1["name"]
    task = celery.send_task('hello.task', args=[name], kwargs={})
    return jsonify(dict(id=task.id, url=url_for('check_task', id=task.id, _external=True)))


@app.route('/check/<string:id>')
def check_task(id):
    task = celery.AsyncResult(id)
    if task.state == 'SUCCESS':
        response = {
            'status': task.state,
            'result': task.result,
            'task_id': id
        }
    elif task.state == 'FAILURE':
        response = json.loads(task.backend.get(task.backend.get_key_for_task(task.id)).decode('utf-8'))
        del response['children']
        del response['traceback']
    else:
        response = {
            'status': task.state,
            'result': task.info,
            'task_id': id
        }
    return jsonify(response)


if __name__ == '__main__':
    app.run()
