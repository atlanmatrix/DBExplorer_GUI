# DBExplorer GUI
An easy-use, light-weight, cross-platform client for bluesky DB.

# Quick start
Run **DBExplorer GUI** on **docker** is suggested, all you need to do is pull 
docker image and run it:
```shell
docker pull yuadocker/dbexplorer
docker run -p 23333:8888 -v /var/run/docker.sock:/var/run/docker.sock -v /usr/bin/docker:/usr/bin/docker -v /tmp:/tmp -d <image_hash|image_name:tag>
```

# Want to run in a non-container environment?
Clone the project to `/srv/www` directory on your machine(CentOS is 
suggested), make `python/python.sh` and files under `python/bin` executable 
like this:
```shell
cd /srv/www/python
chmod 777 python.sh
chmod -R 777 bin/
```

and now, you can run it:
```shell
cd /srv/www
./python/python.sh app.py
```

Log files are located in the **/srv/www/log** directory, if it is not exists,
you need to create one first.
