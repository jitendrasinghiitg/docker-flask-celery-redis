# Dockerized flask-celery-redis 

For flask i have used docker container from :
https://github.com/tiangolo/uwsgi-nginx-flask-docker

## Run on local machine
Install docker and docker-compose
###### Run entire app with one command 
```
sh local_env_up.sh
```
###### content of local_env_up.sh
```
sudo docker-compose -f docker-compose.yml up --scale celery=4 --build
```

It starts a webservice with rest api and listens for messages at localhost:5000

#### Test over REST api

```bash
curl --request POST \
  --url http://localhost:5000/hello_world \
  --header 'content-type: application/json' \
  --data '{
    "name": "jitendra"
  }'
```
**Response**
```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 59
Access-Control-Allow-Origin: *

{
    "id": "cce00e58-9e03-4216-bc68-fa514cf07f7b",
    "url": "http://localhost:5000/check/cce00e58-9e03-4216-bc68-fa514cf07f7b"
}
```
and on hitting above url using curl
```
curl -X GET \
  http://localhost:5000/check/cce00e58-9e03-4216-bc68-fa514cf07f7b 

```
we get status of the task ,and on completion it will return the final output of api

when task is in PROGRESS state we get:
```
{
    "result": {
        "done": 11,
        "total": 60
    },
    "status": "PROGRESS",
    "task_id": "975f0930-c733-41a7-8e94-e9902aef687d"
}
```
when task is in Completed state we get:
```
{
    "result": {
        "result": "hello jitendra"
    },
    "status": "SUCCESS",
    "task_id": "975f0930-c733-41a7-8e94-e9902aef687d"
}
```

when task is in FAILURE state we get:
```
{
    "date_done": "2020-01-02T05:46:38.304535",
    "result": {
        "exc_message": [
            "Traceback (most recent call last):",
            "  File \"/celery_tasks/tasks.py\", line 17, in hello_world",
            "    k = 1 / 0",
            "ZeroDivisionError: division by zero",
            ""
        ],
        "exc_type": "ZeroDivisionError"
    },
    "status": "FAILURE",
    "task_id": "fd6e2e7e-2c97-4841-96c1-abd6e44dba89"
}
```
FAILURE state can be reproduced :
```
curl -X POST \
  http://localhost:5000/hello_world \
  -H 'content-type: application/json' \
  -d '{
	"name":"name"	
}'
```
