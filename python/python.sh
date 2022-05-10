#!/usr/bin/bash

export PYTHONPATH="/srv/www/data/app/DOIM/Server/python/Lib"
export PYTHONPATH="/srv/www/data/app/DOIM/Server/python/DLLs:$PYTHONPATH"
export PYTHONPATH="/srv/www/data/app/DOIM/Server/python/Lib/site-packages:$PYTHONPATH"
export PYTHONPATH="/srv/www/data/app/DOIM/Server/webexpress/python:$PYTHONPATH"
echo $PYTHONPATH
export PYTHONHOME="/srv/www/data/app/DOIM/Server/webexpress/python"
#export PYTHONPATH="/data/app/DOIM/Server/webexpress/python/lib/python3.7/site-packages:$PYTHONPATH"

echo $1 $2 $3 $4 $5
#/usr/bin/python3 $1 $2 $3 $4 $5 $6 $7 $8
/srv/www/data/app/DOIM/Server/python/bin/python3 $1 $2 $3 $4 $5 $6 $7 $8

