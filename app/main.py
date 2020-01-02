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
    Name = input1["name"]
    task = celery.send_task('hello.task', args=[Name], kwargs={})
    return jsonify(dict(id=task.id, url=url_for('check_task', id=task.id, _external=True)))


@app.route('/check/<string:id>')
def check_task(id):
    task = celery.AsyncResult(id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state == 'SUCCESS':
        output = task.result
        return jsonify(output)
    else:
        response = {
            'state': task.state,
            'status': str(task.info)
        }
    return jsonify(response)


if __name__ == '__main__':
    app.run()
