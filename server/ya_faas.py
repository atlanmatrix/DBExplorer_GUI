# @Author: Claude Manchester
# @Time: 2021-12-22
# @Remark: FaaS
import json
import os
import re
import uuid
from time import time
import traceback

from abc import ABC

from config import BASE_URL, FAAS_CODE_DIR, IN_DOCKER_PATH, \
    MAX_FUNC_CODE_LENGTH, MAX_FUNC_NAME_LENGTH
from ya_base import BaseHandler
from utils import convert_object_id


class ListFunc(BaseHandler, ABC):
    def get(self):
        st_ts = time()
        dirname = os.path.dirname(__file__)
        try:
            with open(os.path.join(dirname, 'faas_table.json'), 'r') as fd:
                faas_map = json.load(fd)
                faas_lst = faas_map.values()
        except Exception:
            trace_msg = traceback.format_exc()
            self.logger.error(trace_msg)
            faas_lst = []

        result = '\n\n'.join([
            f'[{faas_obj["name"]}](/faas/{faas_obj["id"]}/edit)'
            for faas_obj in faas_lst
        ])

        return self.write({
            'code': 0,
            'data': result,
            'cost': time() - st_ts
        })


class GetFunc(BaseHandler, ABC):
    def get(self, func_id):
        st_ts = time()
        dirname = os.path.dirname(__file__)
        try:
            with open(os.path.join(dirname, 'faas_table.json'), 'r') as fd:
                faas_map = json.load(fd)
                faas_info = faas_map.get(func_id, {})

                return self.write({
                    'code': 0,
                    'data': faas_info,
                    'cost': time() - st_ts
                })
        except Exception:
            trace_msg = traceback.format_exc()
            self.logger.warn(trace_msg)
            return self.write({
                'code': 0,
                'data': {},
                'cost': time() - st_ts
            })


class CreateFunc(BaseHandler, ABC):
    def get(self):
        # Generate function uuid
        st_ts = time()
        func_id = str(uuid.uuid4())

        return self.write({
            'code': 0,
            'data': func_id,
            'cost': time() - st_ts
        })

    def post(self):
        st_ts = time()
        data = json.loads(self.request.body.decode('utf-8'))
        func_id = data.get('id', None)
        name = data.get('name', func_id)
        code = data.get('code', None)

        if not code:
            return self.write({
                'code': -1,
                'msg': 'Function code is required!',
                'cost': time() - st_ts
            })

        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, 'faas_table.json')

        faas_map = {}
        if not os.path.exists(file_path):
            with open(file_path, 'w') as fd:
                fd.write('{}')

        with open(file_path, 'r+') as fd:
            try:
                faas_map = json.loads(fd.read() or '{}')
            except Exception:
                trace_msg = traceback.format_exc()
                self.logger.error(trace_msg)
                faas_map = {}
            self.logger.info(faas_map)

            for faas_obj in faas_map.values():
                if faas_obj['name'] == name and faas_obj['id'] != func_id:
                    return self.write({
                        'code': -1,
                        'msg': f'Function name {name} already exists!',
                        'cost': time() - st_ts
                    })

            faas_map[func_id] = {
                'id': func_id,
                'name': name,
                'code': code,
            }

            fd.seek(0)
            fd.truncate()
            json.dump(faas_map, fd, indent=4)

        return self.write({
            'code': 0,
            'msg': 'Function created successfully!',
            'cost': time() - st_ts
        })


class RunFunc(BaseHandler, ABC):
    def _update_func(self, func_id, func_info):
        dirname = os.path.dirname(__file__)
        with open(os.path.join(dirname, 'faas_table.json'), 'r') as fd:
            faas_map = json.load(fd)
            faas_map[func_id] = func_info

        with open(os.path.join(dirname, 'faas_table.json'), 'w') as fd:
            json.dump(faas_map, fd, indent=4)

    def get(self, func_id):
        st_ts = time()
        is_test = self.get_argument('is_test', '0')
        enable_cache = self.get_argument('enable_cache', 'false')
        enable_cache = False if enable_cache == 'false' else True

        dirname = os.path.dirname(__file__)
        with open(os.path.join(dirname, 'faas_table.json'), 'r') as fd:
            faas_map = json.load(fd)

        # 1: test mode - find via func_id
        # 0: production mode - find via name
        if is_test == '1':
            faas_info = faas_map.get(func_id, None)
        else:
            for faas_id, faas_obj in faas_map.items():
                if faas_obj['name'] == func_id:
                    faas_info = faas_obj
                    func_id = faas_id
                    break
            else:
                faas_info = None

        if faas_info is None:
            return self.write({
                'code': -1,
                'msg': 'Function not found!',
                'cost': time() - st_ts
            })

        if is_test == '0' and \
                faas_info.get('enable_cache', None) and\
                faas_info.get('cache', None):
            return self.write(faas_info['cache'])

        code = faas_info.get('code', '')

        tmpl_path = os.path.join(dirname, 'faas_tmpl.py')

        with open(tmpl_path) as fd:
            tmpl_data = fd.read()

        try:
            res = re.search(r'def (.*)\(.*\):', code)
            func_name = res.groups()[0]
        except AttributeError:
            return self.write({
                'code': -1,
                'msg': 'Invalid grammar!',
                'cost': time() - st_ts
            })

        dst_data = tmpl_data.replace(
            '#$name$', func_name).replace(
            '#$code$', f'#$$\n{code}\n#$$').replace(
            '#@faas_func_wrapper', '@faas_func_wrapper')
        dist_path = os.path.join(FAAS_CODE_DIR, f'{func_id}.py')
        with open(dist_path, 'w') as fd:
            fd.write(dst_data)

        docker_cmd = (f'docker run --rm --name my-running-script '
            f'-v {FAAS_CODE_DIR}:{IN_DOCKER_PATH} '
            f'-w {IN_DOCKER_PATH} python python {func_id}.py')
        self.logger.info(docker_cmd)
        log_data = os.popen(docker_cmd).read()
        self.logger.info(log_data)

        if is_test == '0':
            # Call function
            log_data = log_data.split('\nStatus:\n')[0].split('\nReturn:\n')[1]
        else:
            # Test function
            try:
                log = log_data.split('\nStatus:\n')[0].split('\nReturn:\n')[0].split('Print Log:\n')[1]
                ret = log_data.split('\nStatus:\n')[0].split('\nReturn:\n')[1]
                res = log_data.split('\nStatus:\n')[1].strip('\n')

                res_code = 0

                msg = 'success'
                if res == 'error':
                    res_code = -1
                    msg = 'An error occurred while executing your function!'
                log_data = json.dumps({
                    'code': res_code,
                    'msg': msg,
                    'data': {
                        'log': log,
                        'ret': ret
                    },
                    'cost': time() - st_ts
                })
                faas_info.update({
                    'enable_cache': enable_cache,
                    'cache': ret
                })
                self._update_func(func_id, faas_info)
            except Exception:
                trace_msg = traceback.format_exc()
                self.logger.error(trace_msg)
                log_data = json.dumps({
                    'code': -1,
                    'msg': 'System Error',
                    'cost': time() - st_ts
                })
        return self.write(log_data)
