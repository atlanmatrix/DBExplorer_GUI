# @Author: Claude Manchester
# @Time: 2021-12-10
# @Remark: base
import os
from time import time
from typing import Any
import logging
from functools import wraps

from tornado import httputil
import tornado.web

from config import MODE, LOG_PATH
from ya_mongo import YaMongoDB


if MODE == 'DEBUG':
    log_level = logging.DEBUG
else:
    log_level = logging.INFO

if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

logging.basicConfig(
    filename=LOG_PATH,
    level=log_level,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')

time_handler = logging.handlers.TimedRotatingFileHandler(LOG_PATH, when='d',
                                                         interval=1)


def ya_cost(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.cost_start = time()
        return func(self, *args, **kwargs)
    return wrapper


class BaseHandler(tornado.web.RequestHandler, YaMongoDB):
    def __init__(self, application: "tornado.web.Application",
                 request: httputil.HTTPServerRequest, **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
        self.logger = logging
        self.set_cookie('abc', 'def')
        self.set_header("Access-Control-Allow-Origin", "*") # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        logging.getLogger().addHandler(time_handler)

    def ya_ok(self, data=None, msg='success'):
        return self.write({
            'code': 0,
            'data': data,
            'msg': msg,
            'cost': time() - self.cost_start
        })

    def ya_error(self, msg='system error', code=-1):
        return self.write({
            'code': code,
            'msg': msg,
            'cost': time() - self.cost_start
        })

    def write_error(self, status_code: int, **kwargs: Any) -> None:
        if status_code == 400:
            self.response(status_code,
                          'Missing argument')
        elif status_code == 403:
            self.response(status_code,
                          'Permission denied')
        elif status_code == 404:
            self.response(status_code,
                          'Resource not found. Check the URL.')
        elif status_code == 405:
            self.response(status_code,
                          'Method not allowed in this resource.')
        elif status_code == 500:
            self.set_status(status_code)
            self.render('500.html')
        else:
            self.response(status_code,
                          'Internal server error on specific module.')
