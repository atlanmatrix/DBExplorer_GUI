FROM node:8.9.1-alpine
ENV LD_LIBRARY_PATH="/srv/www/libs/"
WORKDIR /srv/www
COPY . .
COPY client/dist ./dist
EXPOSE 8888
CMD ["/srv/www/python/python.sh", "/srv/www/app.py"]
