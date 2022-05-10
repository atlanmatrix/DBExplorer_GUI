# Deploy DB-Explorer on Your Machine(Unfinished)
---
Currently **only** supports CentOS system! **But** you can try to deploy it manually on Windows machine, which is theoretically possible.


## Deploy on Docker
Docker official installation documention: ([https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/))


### I. Install Latest Docker

```bash
# 1. Uninstall old versions
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine

# 2. Set up the repository
sudo yum install -y yum-utils
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo

# 3. Install Docker Engine
sudo yum install docker-ce docker-ce-cli containerd.io

# 4. Start Docker.
sudo systemctl start docker

# 5. Verify
sudo docker run hello-world
```

### II.Get Docker Image of Python

```bash
docker pull python
```


### III.Get **DB Explorer** docker image(or tar.gz)

```
# Pull image from repository
# Coming soon...

# Load image throught tar.gz
docker load -i <image_name>.tar.gz
```


### IV.Run

```bash
docker run -p 23333:8888 -v /var/run/docker.sock:/var/run/docker.sock -v /usr/bin/docker:/usr/bin/docker -v /tmp:/tmp -d <image_hash|image_name:tag>
```


### V.Try it!

Open your browser(such as chrome, edge...),and visit 

```bash
http://{host}:23333/<db_server>/db/tree

# such as:
# http://192.168.8.188:23333/demo.jiankongyi.com/db/tree
```



## Advanced

Rebuild image:
```bash
docker build -t <image_name:tag> .
```

Save image:
```bash
docker save <image_name:tag> | gzip > <image_name>.tar.gz
```

Write plugin:
```
# Coming soon...
```
