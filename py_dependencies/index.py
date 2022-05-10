import pdb
import importlib
import os
import sys
import traceback
import time
from configparser import ConfigParser

from mxsoftpy.def_http_code import WeMr
from mxsoftpy.exception import NotFoundError

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + os.sep + 'pyweb')

from utils.conf.mxconfig import MxConfig  # 导入配置
from utils.conf.mxlog import setup_log
from utils.conf.i18n import setup_language
from utils.public.mini_cache import MiniCache

# 全局flag，用于判断是否是初次请求，只有初次请求会实例化app
flag = False

# 框架入口
app = None

# 国际化支持
_ = None

# 缓存
# mini_cache = MiniCache()


def register_extensions(mx):
    """
    注册组件
    """
    from utils.middleware.before_request import cross_domain
    from utils.conf.register_module import register_module

    mx.before_request(cross_domain)
    register_module(app)


def create_app():
    """
    创建应用
    """
    global app
    global _
    from mxsoftpy import Mx
    app = Mx()
    setup_log(MxConfig.LOG_LEVEL)  # 配置日志
    _ = setup_language(MxConfig.LANGUAGES)  # 配置语言

    register_extensions(app)
    return app


def run(session):
    global flag
    global app
    if flag:
        pass
    else:
        app = create_app()
        flag = True
    #pdb.set_trace()
    try:
        try:
            app(session)
            return WeMr.WE_MR_OK
        except NotFoundError:
            url = session.GetUrl()

            # 获取请求路径
            path = url.GetPath()

            # url, prefix_ = path.split(".sy")
            if path.find('sy') > 0:
                urlno, prefix_ = path.split(".sy")
                urls = urlno.split("/")
            else:
                urls = path.split("/")
            # urls = url.split("/")
            num = len(urls) - 1
            active = urls[num]
            urls.pop(num)

            szMod = urls.pop(0)

            modules = ".".join(urls)
            modules = szMod + '.controller.' + modules

            obj = importlib.import_module('.', modules)

            # 判断是否需要重新加载文件
            reload = False
            cfg = ConfigParser()
            cfg.read(os.path.dirname(__file__) + '/conf/Pyconf.ini')
            if cfg.get('reload', 'reloadNum') == '1':
                reload = True

            # 调用模块方法
            if hasattr(obj, active):
                if reload:
                    obj = importlib.reload(obj)
                func = getattr(obj, active)
                func(session)
                return WeMr.WE_MR_OK
            else:
                if reload:
                    obj = importlib.reload(obj)
                class_ = getattr(obj, urls[int(num) - 2])
                cls = class_(session)
                attr_obj = getattr(cls, active)
                if hasattr(attr_obj, '__call__'):
                    attr_obj()

                return WeMr.WE_MR_OK
            # raise NotFoundError()

    except Exception:
        log_name = time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
        path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/middle/Pymod/'
        if not os.path.exists(path):
            os.makedirs(path)
        traceback.print_exc(file=open(path + log_name, 'w+'))
        return WeMr.WE_MR_FAILED
