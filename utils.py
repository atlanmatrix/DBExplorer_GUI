# @Author: Claude Manchester
# @Time: 2021-12-15
# @Remark: Utils
import base64
import functools
import json
import os
import time
import traceback
from hashlib import sha256

from tornado.web import HTTPError
from tornado.web import RequestHandler

from config import DB_DIR


def token_checker(func):
    @functools.wraps(func)
    def wrapper(self: RequestHandler, *args, **kwargs):
        path = self.request.path

        for router in ['/file', '/doc', '/upload']:
            if path.startswith(router):
                need_auth = True
                break
        else:
            need_auth = False

        if need_auth:
            app_key = self.get_argument('app_key', '')
            token_like = self.get_argument('token', '')
            res, msg = check_token(app_key, router, token_like)
            if not res:
                raise HTTPError(403)
        return func(self, *args, **kwargs)
    return wrapper


def check_token(app_key, path, token_like):
    try:
        with open(os.path.join(DB_DIR, 'user.json')) as fd:
            user_json = json.load(fd)

        if app_key not in user_json:
            raise ValueError("Invalid App Key")

        user_data = user_json[app_key]

        access = user_data['access']
        if path not in access:
            raise ValueError('Invalid Access')

        expire = access[path]['expire']
        secret = user_data['secret']
        now = int(time.time())

        # Parse ts part
        b64_hex_ts = token_like[:6] + token_like[-6:]
        hex_ts = base64.b64decode(b64_hex_ts)
        ts = int(hex_ts, 16)

        m = sha256()
        m.update(str.encode(app_key))
        m.update(str.encode(secret))
        m.update(str.encode(b64_hex_ts))
        hashed_ts_token = m.hexdigest()
        token = token_like[6:-6]

        if hashed_ts_token != token:
            raise ValueError('Invalid Token')

        # Parse token part
        if now - ts > expire:
            raise ValueError('Token Expired')
        return True, 'ok'
    except ValueError as err:
        return False, err
    except Exception:
        return False, 'System Error'


def convert_object_id(doc_lst):
    new_doc_lst = []
    for doc in doc_lst:
        doc['_id'] = str(doc['_id'])
        new_doc_lst.append(doc)
    return new_doc_lst


def ts_to_date(ts):
    pass


def date_to_ts(date):
    pass
