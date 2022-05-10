FROM centos:7
ENV LD_LIBRARY_PATH="/srv/www/data/app/DOIM/Server/bin/python/lib/:/srv/www/data/app/DOIM/Server/python/:/srv/www/data/app/DOIM/Server/webexpress/:/srv/www/data/app/DOIM/Server/bin/"
WORKDIR /
COPY /data .
WORKDIR /srv/www
COPY . .
CMD ["/srv/www/data/app/DOIM/Server/python/python.sh", "app.py"]

