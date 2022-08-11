#!/usr/bin/bash

export PYTHONPATH="/srv/www/python/Lib"
export PYTHONPATH="/srv/www/python/DLLs:$PYTHONPATH"
export PYTHONPATH="/srv/www/python/Lib/site-packages:$PYTHONPATH"
export PYTHONPATH="/srv/www/py_dependencies:$PYTHONPATH"
export PYTHONHOME="/srv/www/python"
export LD_LIBRARY_PATH="/srv/www/libs/"

/srv/www/python/bin/python3 $1 $2 $3 $4 $5 $6 $7 $8

