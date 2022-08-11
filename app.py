"""
Http server of DBExplorer
"""
import os
import json
import traceback
from time import time

import tornado.ioloop
import tornado.web

from superbsapi import bs_treedb_query_mainkeys
from jkyweb.module.public.TreeModel import TreeModel
from config import __VERSION__
from ya_base import BaseHandler, ya_cost
from ya_file import FileUploader, FileDownloader, MDFileViewer
from ya_faas import ListFunc, CreateFunc, RunFunc, GetFunc


class MainHandler(BaseHandler):
    def get(self):
        return self.render('index.html')


class TreeDBHandler(BaseHandler):
    """
    Get tree db sub keys and key properties
    """
    def post(self):
        st_ts = time()
        # bs_treedb_query_mainkeys(a_r, 'master', 'demo.jiankongyi.com', 8123)
        host = self.get_argument('host')
        port = self.get_argument('port', 8123)
        filename = self.get_argument('filename', None)

        if filename is None:
            file_lst = ['ccubase', 'base', 'master', 'Co_1', 'ipctrl']

            config_path = os.path.join(
                os.path.dirname(__file__), 'webConfig.json')

            with open(config_path, 'r') as fd:
                config_data = json.load(fd)
                for config_item in config_data['host']:
                    if config_item['host'] == host:
                        file_lst = [
                            item['name'] for item in config_item['dbFiles']]
                        break

            return self.write({
                'code': 0,
                'data': {
                    'sub_keys': [{
                        'path': key,
                        'label': key,
                        'children': []
                        } for key in file_lst],
                    'props': []
                },
                'cost': time() - st_ts
            })

        path = self.get_argument('path', '')
        path_lst = path.split('\\')

        if not path:
            main_key_lst = []
            bs_treedb_query_mainkeys(main_key_lst, filename, host, port)
            return self.write({
                'code': 0,
                'data': {
                    'sub_keys': [{
                        'path': f'{filename}\\{key}',
                        'label': key,
                        'children': []
                        } for key in main_key_lst],
                    'props': []
                },
                'cost': time() - st_ts
            })

        main_key, *sub_key_lst = path_lst
        db = TreeModel()
        print(main_key, '\\'.join(sub_key_lst), host, filename)
        sub_keys = db.open(main_key, '\\'.join(sub_key_lst), host, filename).sub_keys()
        sub_keys = [{
            'label': key,
            'children': [],
            'path': f'{filename}\\{path}\\{key}'
        } for key in sub_keys]
        props = db.open(main_key, '\\'.join(sub_key_lst), host, filename).items()

        return self.write({
            'code': 0,
            'data': {
                'sub_keys': sub_keys,
                'props': [{
                    'name': field_name,
                    'type': '',
                    'value': field_value,
                } for field_name, field_value in props.items()]
            },
            'cost': time() - st_ts
        })


class TreeDBAddSubkeyHandler(BaseHandler):
    """
    Add sub key of treeDB
    """
    def post(self):
        st_ts = time()
        db = TreeModel()

        try:
            data = json.loads(self.request.body.decode('utf-8'))
            host = data.get('host', None)
            path = data.get('path', None)
            sub_key = data.get('sub_key', None)
        except Exception:
            host = self.get_argument('host', None)
            path = self.get_argument('path', None)
            sub_key = self.get_argument('sub_key', None)

        path_lst = path.split('\\')

        try:
            filename, main_key, *sub_key_lst = path_lst
        except Exception:
            trace_msg = traceback.format_exc()
            self.logger.error(trace_msg)
            return self.write({
                'code': -1,
                'msg': 'Invalid path parameter',
                'cost': time() - st_ts
            })

        try:
            db.open(
                main_key,
                '\\'.join(sub_key_lst),
                host,
                filename
            ).insert_sub_key(sub_key)

            return self.write({
                'code': 0,
                'cost': time() - st_ts
            })
        except Exception:
            trace_msg = traceback.format_exc()
            self.logger.error(trace_msg)
            return self.write({
                'code': -1,
                'msg': 'Add sub key failed',
                'cost': time() - st_ts
            })


class TreeDBUpdateKeyHandler(BaseHandler):
    """
    Update sub key of treeDB
    """
    def post(self):
        st_ts = time()
        db = TreeModel()

        try:
            data = json.loads(self.request.body.decode('utf-8'))
            host = data.get('host', None)
            path = data.get('path', None)
            sub_key = data.get('sub_key', None)
        except Exception:
            host = self.get_argument('host', None)
            path = self.get_argument('path', None)
            sub_key = self.get_argument('sub_key', None)

        path_lst = path.split('\\')
        print(path_lst)
        try:
            filename, main_key, *sub_key_lst = path_lst
        except Exception:
            trace_msg = traceback.format_exc()
            self.logger.error(trace_msg)
            return self.write({
                'code': -1,
                'msg': 'Invalid path parameter',
                'cost': time() - st_ts
            })

        try:
            db.open(
                main_key,
                '\\'.join(sub_key_lst),
                host,
                filename
            ).rename(sub_key, None)

            return self.write({
                'code': 0,
                'cost': time() - st_ts
            })
        except Exception:
            trace_msg = traceback.format_exc()
            self.logger.error(trace_msg)
            return self.write({
                'code': -1,
                'msg': 'Edit key failed',
                'cost': time() - st_ts
            })


class TreeDBDeleteKeyHandler(BaseHandler):
    """
    Delete sub key of treeDB
    """
    def post(self):
        st_ts = time()
        db = TreeModel()

        try:
            data = json.loads(self.request.body.decode('utf-8'))
            host = data.get('host', None)
            path = data.get('path', None)
        except Exception:
            host = self.get_argument('host', None)
            path = self.get_argument('path', None)

        self.logger.info(path)
        path_lst = path.split('\\')

        try:
            filename, main_key, *sub_key_lst = path_lst
        except Exception:
            trace_msg = traceback.format_exc()
            self.logger.error(trace_msg)
            return self.write({
                'code': -1,
                'msg': 'Invalid path parameter',
                'cost': time() - st_ts
            })

        try:
            db.open(
                main_key,
                '\\'.join(sub_key_lst),
                host,
                filename
            ).delete()

            return self.write({
                'code': 0,
                'cost': time() - st_ts
            })
        except Exception:
            trace_msg = traceback.format_exc()
            self.logger.error(trace_msg)
            return self.write({
                'code': -1,
                'msg': 'Delete key failed',
                'cost': time() - st_ts
            })


class TreeDBSearchHandler(BaseHandler):
    """
    Search treeDB
    """
    def _group_recursion(self, group_sub_items):
        for group in group_sub_items:
            tmp_group = group_sub_items[group]

            path = [tmp_group['mxlabel']]
            self.logger.info('/' * 50)
            while tmp_group['mxparent'] != '1.TS.1':
                self.logger.info(tmp_group['mxlabel'])
                tmp_group = group_sub_items[tmp_group['mxparent']]
                path.insert(0, tmp_group['mxlabel'])
            group_sub_items[group]['path'] = '\\'.join(path)
        self.logger.info(group_sub_items)
        return group_sub_items

    def post(self):
        st_ts = time()
        data = json.loads(self.request.body.decode('utf-8'))
        host = data.get('host', None)
        # 0 - device   1 - plugin
        # device ip/label
        search_text = data.get('search_text', '')

        db = TreeModel()
        result = {
            'device': [],
            'plugin': [],
            'group': [],
        }
        # Search device
        ccu_lst = db.open('Co', r'Co_1\CCUList', host, 'master').sub_keys()
        for ccu in ccu_lst:
            dev_sub_key_items = db.open(ccu, r'1\1.SD', host, 'ccubase').sub_items()
            for sub_key in dev_sub_key_items:
                key_item = dev_sub_key_items[sub_key]
                label = key_item.get('mxlabel', '')
                db_server_ip = key_item.get('_target_ip', '')
                device_type = key_item.get('mxdevicetype', '')
                if search_text in label or search_text in db_server_ip or search_text in device_type:
                    result['device'].append({
                        'id': sub_key,
                        'label': label,
                        'ip': db_server_ip,
                        'device_type': device_type,
                        'path': f'{ccu}\\1\\1.SD\\{sub_key}'
                    })

            group_sub_key_items = db.open(ccu, r'1\1.SG', host, 'ccubase').sub_items()
            for sub_key in group_sub_key_items:
                key_item = group_sub_key_items[sub_key]
                label = key_item.get('mxlabel', '')
                path = key_item.get('path', '')
                if search_text in label:
                    result['group'].append({
                        'id': sub_key,
                        'label': label,
                        'path': f'{ccu}\\1.TS.1\\{path}'
                    })
        # Search PluginData
        plugin_sub_keys = db.open('PluginData', '', host, 'base').sub_keys()
        for sub_key in plugin_sub_keys:
            if search_text in sub_key:
                result['plugin'].append({
                    'id': sub_key,
                    'path': f'base\\PluginData\\{sub_key}'
                })
        return self.write({
            'code': 0,
            'data': result,
            'cost': time() - st_ts
        })


class TreeDBPropsHandler(BaseHandler):
    """
    Get treeDB key properties
    """
    def post(self):
        st_ts = time()
        db = TreeModel()

        data = json.loads(self.request.body.decode('utf-8'))
        host = data.get('host', None)
        path = data.get('path', None)

        path_lst = path.split('\\')
        print(path_lst)
        try:
            filename, main_key, *sub_key_lst = path_lst
        except Exception:
            trace_msg = traceback.format_exc()
            self.logger.error(trace_msg)
            return self.write({
                'code': -1,
                'msg': 'Invalid path parameter',
                'cost': time() - st_ts
            })

        try:
            items = db.open(
                main_key,
                '\\'.join(sub_key_lst),
                host,
                filename
            ).items()

            return self.write({
                'code': 0,
                'data': items,
                'cost': time() - st_ts,
            })
        except Exception:
            trace_msg = traceback.format_exc()
            self.logger.error(trace_msg)
            return self.write({
                'code': -1,
                'msg': 'Get property failed',
                'cost': time() - st_ts
            })


class TreeDBUpdatePropHandler(BaseHandler):
    """
    Update treeDB key property
    """
    def post(self):
        st_ts = time()
        db = TreeModel()

        try:
            data = json.loads(self.request.body.decode('utf-8'))
            host = data.get('host', None)
            path = data.get('path', None)
            prop_name = data.get('prop_name', None)
            prop_val = data.get('prop_val', None)
        except Exception:
            host = self.get_argument('host', None)
            path = self.get_argument('path', None)
            prop_name = self.get_argument('prop_name', None)
            prop_val = self.get_argument('prop_val', None)

        path_lst = path.split('\\')
        self.logger.debug(f'host: "{host}" path: "{path}" '
                          f'prop_name: "{prop_name}" prop_val: "{prop_val}"')
        try:
            filename, main_key, *sub_key_lst = path_lst
        except Exception:
            trace_msg = traceback.format_exc()
            self.logger.error(trace_msg)
            return self.write({
                'code': -1,
                'msg': 'Invalid path parameter',
                'cost': time() - st_ts
            })

        try:
            db.open(
                main_key,
                '\\'.join(sub_key_lst),
                host,
                filename
            ).insert_items([(prop_name, prop_val)])

            properties = db.open(
                main_key,
                '\\'.join(sub_key_lst),
                host,
                filename
            ).items()

            return self.write({
                'code': 0,
                'data': [{
                    'name': key,
                    'value': val
                } for key, val in properties.items()],
                'cost': time() - st_ts,
            })
        except Exception:
            trace_msg = traceback.format_exc()
            self.logger.error(trace_msg)
            return self.write({
                'code': -1,
                'msg': 'Update property failed',
                'cost': time() - st_ts
            })


class TreeDBDeletePropHandler(BaseHandler):
    @ya_cost
    def post(self):
        host = self.get_argument('host', None)
        path = self.get_argument('path', None)
        prop_name = self.get_argument('prop_name', None)

        db = TreeModel()
        try:
            filename, main_key, *sub_key_lst = path
            db.open(main_key, '\\'.join(sub_key_lst), host, filename)
            db.delete_prop(prop_name)
        except Exception as e:
            return self.ya_error(str(e))
        else:
            return self.ya_ok('ok')


class TreeDBAutoCodeHandler(BaseHandler):
    """
    Auto generate CRUD code
    """
    def post(self):
        st_ts = time()
        data = json.loads(self.request.body.decode('utf-8'))
        host = data.get('host', None)
        path = data.get('path', None)

        path_lst = path.split('\\')

        try:
            filename, main_key, *sub_key_lst = path_lst
        except Exception:
            trace_msg = traceback.format_exc()
            self.logger.error(trace_msg)
            return self.write({
                'code': -1,
                'msg': 'Invalid path parameter',
                'cost': time() - st_ts
            })

        sub_key = '\\'.join(sub_key_lst)
        try:
            real_path = os.path.join(
                os.path.dirname(__file__),
                'docs/autoCodeTemplate.md'
            )
            with open(real_path, 'r', encoding='utf-8') as fd:
                data = fd.read()

            data = data.replace('$$HOST$$', host
                ).replace('$$MAIN_KEY$$', main_key
                ).replace('$$SUB_KEY$$', sub_key
                ).replace('$$FILENAME$$', filename)

            return self.write({
                'code': 0,
                'data': data,
                'cost': time() - st_ts
            })
        except Exception:
            trace_msg = traceback.format_exc()
            self.logger.error(trace_msg)
            return self.write({
                'code': -1,
                'msg': 'Automatically generate code failed(2)',
                'cost': time() - st_ts
            })


class ConfigurationManage(BaseHandler):
    """
    Configure handler of web app
    """
    @ya_cost
    def get(self, cfg_name):
        # load config file
        try:
            config_path = os.path.join(
                os.path.dirname(__file__), 'webConfig.json')
            with open(config_path, 'r', encoding='utf-8') as fd:
                config_data = json.load(fd)
        except Exception:
            return self.ya_error('Load configuration json error')

        # check config name
        if cfg_name not in config_data:
            return self.ya_error('Invalid configuration entry')

        # get specific config or update value of one config
        return self.ya_ok(config_data[cfg_name])

    @ya_cost
    def post(self, cfg_name):
        req_body = json.loads(self.request.body.decode('utf-8'))
        op = req_body.get('op', 'get')

        # load config file
        try:
            config_path = os.path.join(
                os.path.dirname(__file__), 'webConfig.json')
            with open(config_path, 'r', encoding='utf-8') as fd:
                config_data = json.load(fd)
        except Exception:
            return self.ya_error('Load configuration json error')

        # check config name
        if cfg_name not in config_data:
            return self.ya_error('Invalid configuration entry')

        # get specific config or update value of one config
        if op == 'get':
            return self.ya_ok(config_data[cfg_name])

        if op == 'update':
            updated_cfg_data = req_body.get('data', None)
            config_data[cfg_name] = updated_cfg_data
            self.logger.info(config_data)
            with open(config_path, 'w', encoding='utf-8') as fd:
                json.dump(config_data, fd)
            return self.ya_ok(None, 'Updated successfully')

        return self.ya_error('Invalid operation')


class SysInfoManage(BaseHandler):
    @ya_cost
    def get(self):
        sys_info = {
            'ver': __VERSION__
        }

        return self.ya_ok(sys_info)

    def post(self):
        pass


def make_app():
    """
    Main app
    """
    template_path = os.path.join(os.path.dirname(__file__), "dist")
    static_path = os.path.join(os.path.dirname(__file__), "dist/src")
    js_path = os.path.join(static_path, 'assets/js')
    css_path = os.path.join(static_path, 'assets/css')
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/src/assets/js/(.*)", tornado.web.StaticFileHandler, {"path": js_path}),
        (r"/src/assets/css/(.*)", tornado.web.StaticFileHandler, {"path": css_path}),
        # File handlers
        (r"/upload", FileUploader),
        (r"/file/(.*)", FileDownloader),
        (r"/api/doc/md/(.*)", MDFileViewer),
        # DB key
        (r"/api/db/tree", TreeDBHandler),
        (r"/api/db/tree/add", TreeDBAddSubkeyHandler),
        (r"/api/db/tree/update", TreeDBUpdateKeyHandler),
        (r"/api/db/tree/duplicate", TreeDBUpdateKeyHandler),
        (r"/api/db/tree/delete", TreeDBDeleteKeyHandler),
        (r"/api/db/tree/search", TreeDBSearchHandler),
        # DB properties
        (r"/api/db/tree/props", TreeDBPropsHandler),
        (r"/api/db/tree/props/add", TreeDBDeleteKeyHandler),
        (r"/api/db/tree/props/update", TreeDBUpdatePropHandler),
        (r"/api/db/tree/props/duplicate", TreeDBDeleteKeyHandler),
        (r"/api/db/tree/props/delete", TreeDBDeletePropHandler),
        # Auto code
        (r"/api/db/tree/auto_code", TreeDBAutoCodeHandler),
        # Faas
        (r"/api/faas/list", ListFunc),
        (r"/api/faas/create", CreateFunc),
        (r"/api/faas/(.*)/info", GetFunc),
        (r"/api/faas/(.*)", RunFunc),
        # Configuration
        (r"/api/cfg/(.*)", ConfigurationManage),
        # Others
        (r"/api/sys/info", SysInfoManage),
        # Finally
        (r"/.*", MainHandler),
    ],
        template_path=template_path,
        static_path=static_path,
        static_url_prefix='/yua-static/',
        debug=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
