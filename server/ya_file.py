# @Author: Claude Manchester
# @Time: 2021-12-14
# @Remark: File
import os
import logging
import urllib
import traceback
from time import time
from abc import ABC

import markdown

from config import UPLOAD_DIR
from config import TEXT_SUFFIX, IMG_SUFFIX, VIDEO_SUFFIX, MD_SUFFIX
from ya_base import BaseHandler
from utils import token_checker


class FileUploader(BaseHandler, ABC):
    @token_checker
    def post(self):
        path = self.get_argument('path', '')
        real_path = os.path.join(UPLOAD_DIR, path)

        if not os.path.exists(real_path):
            os.makedirs(real_path)

        uploaded_lst = []
        for field_name, files in self.request.files.items():
            for info in files:
                filename, content_type = info['filename'], info['content_type']
                body = info['body']
                logging.info('%s', os.getcwd())
                file_path = os.path.join(real_path, filename)
                f = open(file_path, 'wb')
                f.write(body)
                f.close()
                dir_lst = path.split('/') + [filename]
                dir_lst = list(map(lambda x: urllib.parse.quote_plus(x),
                                   dir_lst))
                uploaded_lst.append(os.path.join(*dir_lst).replace('+', '%20'))

        return self.write({
            'status': True,
            'msg': uploaded_lst
        })


class FileDownloader(BaseHandler, ABC):
    @token_checker
    def get(self, filename):
        buf_size = 4096
        basename = os.path.basename(filename)
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + basename)
        with open(rf'{UPLOAD_DIR}{filename}', 'rb') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                self.write(data)
        self.finish()


class MDFileViewer(BaseHandler, ABC):
    def get(self, path):
        st_ts = time()
        try:
            real_path = os.path.join(
                os.path.dirname(__file__),
                f'../docs/{path}'
            )
            with open(real_path, 'r', encoding='utf-8') as fd:
                data = fd.read()
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
                'msg': '# Oh! No! Something error...\n\n Documention not exists',
                'cost': time() - st_ts
            })


class FileViewer(BaseHandler, ABC):
    # @token_checker
    def get(self, path):
        app_key = self.get_argument('app_key', '')
        token = self.get_argument('token', '')
        suffix = os.path.splitext(path)[-1]
        filename = os.path.split(path)[-1]

        if os.path.exists(f'docs/{path}'):
            real_path = f'docs/{path}'
        else:
            real_path = rf'{UPLOAD_DIR}{path}'

        kwargs = {
            "app_key": app_key,
            "token": token,
            "path": path,
            "filename": filename,
        }

        if not os.path.isfile(real_path):
            return self.render('NoViewerOrInvalid.html', **kwargs)

        if suffix in TEXT_SUFFIX:
            with open(real_path, 'r', encoding='utf-8') as fd:
                data = fd.read()

            kwargs.update({
                "class_name": TEXT_SUFFIX[suffix],
                "data": data
            })
            return self.render('PureTextFileViewer.html', **kwargs)
        if suffix in IMG_SUFFIX + VIDEO_SUFFIX:
            return self.render('UnderDev.html', **kwargs)
        if suffix in MD_SUFFIX:
            with open(real_path, 'r', encoding='utf-8') as fd:
                data = fd.read()
            html_str = markdown.markdown(data, extensions=[
                'tables',
                'markdown.extensions.extra'])
            kwargs.update({
                "html_str": html_str
            })
            return self.render('MDFileViewer.html', **kwargs)
        return self.render('DownloadPage.html', **kwargs)
