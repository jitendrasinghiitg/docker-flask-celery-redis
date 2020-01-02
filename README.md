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
sudo docker-compose -f docker-compose.yml up -d --build
```

It starts a webservice with rest api and listens for messages at localhost:5000

#### Test over REST api

```bash
curl --request POST \
  --url http://localhost:5000/hello_world \
  --header 'content-type: application/json' \
  --data '{
    "message": "jitendra"
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

when task is in PROGRESS we get:
```
{
    "state": "PROGRESS",
    "status": "{'done': 5, 'total': 60}"
}
```
when task is in Completed we get:
```
{
    "result": "hello jitendra",
    "status": "COMPLETED"
}
```

