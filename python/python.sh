#!/usr/bin/bash

export PYTHONPATH="/srv/www/python/Lib"
export PYTHONPATH="/srv/www/python/DLLs:$PYTHONPATH"
export PYTHONPATH="/srv/www/python/Lib/site-packages:$PYTHONPATH"
export PYTHONPATH="/srv/www/py_dependencies"
export PYTHONHOME="/srv/www/python"

/srv/www/python/bin/python3 $1 $2 $3 $4 $5 $6 $7 $8

