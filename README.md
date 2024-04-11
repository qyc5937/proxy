# build docker containers
docker-compose build --no-cache

# Run docker containers
docker-compose up

# Listing all running docker containers
docker ps

# Getting a shell into a running docker container
docker exec -it <CONTAINER ID> /bin/sh

# assuming the response from docker ps is

```
└─(19:30:12)──> docker ps                                                  130 ↵ ──(Wed,Apr10)─┘
CONTAINER ID   IMAGE           COMMAND                  CREATED         STATUS         PORTS                      NAMES
8e890bd2e85f   proxytest-web   "pipenv run python3 …"   2 minutes ago   Up 6 seconds   0.0.0.0:12504->12504/tcp   proxytest-web-1
```

then the command will be
docker exec -it 8e890bd2e85f /bin/sh


#docker cheat sheet
https://docs.docker.com/get-started/docker_cheatsheet.pdf
https://devhints.io/docker-compose

