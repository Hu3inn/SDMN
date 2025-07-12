### 1-Building the docker image


```
sudo sh -c 'docker build -t status-server .'
```


### 2-Run the container


```
sudo sh -c 'docker run -d -p 8000:8000 --name myserver status-server'
#myserver is the name, can be anything you want
```


### 3-API test


```
# GET: requesting the satus from the address
curl localhost:8000/api/v1/status
# must show: → { "status": "OK" }

# POST: changing the status
curl -X POST -H "Content-Type: application/json" \
    -d '{"status": "not OK"}' \
    localhost:8000/api/v1/status
#must show: → { "status": "not OK" }
# if you want the status to show anything else, change -d '' argument.
# every time you post (change) it gives 201, and every time you just Get (request the current status) it gives 200

# GET again
curl localhost:8000/api/v1/status
#must show: → { "status": "not OK" }
```


### some extra docker command for checking and testing

```
sudo sh -c 'docker ps'
#list running container

sudo sh -c 'docker stop <container_name>'
#stop the container specified

sudo sh -c 'docker rm <container_name>'
#when i changed sth about the my httpserver in app.py, and after rebuilding it, when i tried to run the container, it gave me a error saying that said container name is in used, so in order to rerun the container with the same name we should remove the previously ran container
