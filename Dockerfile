FROM centos:7
ENV LD_LIBRARY_PATH="/srv/www/libs/"
WORKDIR /srv/www
COPY . .
RUN cd client && yarn install && yarn build
COPY client/dist ./dist
EXPOSE 8888
CMD ["/srv/www/python/python.sh", "/srv/www/app.py"]
