from BSWork import *
import sys
import math
import os

"""公共基类"""


class BasePy(object):

    def __init__(self, pSession):
        nRet, callbackparam, param = SessionInit(pSession, False, False)
        nRet, postData = pSession.GetPostString()
        nRet, callbackparam, post = SessionInit(pSession, False, True)
        self.postData = postData
        self.param = {**param, **post}
        self.callback = callbackparam
        self._sHostName = '127.0.0.1'
        self._uPort = 8123
        self.pSession = pSession

    @staticmethod
    def get_web_path():
        """
        返回当前目录
        :return:
        """
        return os.path.dirname(os.path.dirname(__file__))

    def mx_error(self, errmsg):
        """
        返回错误的json
        :param errmsg: 错误消息
        :return: json格式
        """
        error = {'status': 'failed', 'errmsg': errmsg}
        # error.encode('utf-8').strip()
        sys.stdout.flush()
        print(errmsg)
        print(error)
        json_str = json.dumps(error, ensure_ascii=False)

        SendInfoToWebWithCallback(self.pSession, self.callback, json_str)

    def mx_success(self, errmsg, data, type=None):
        """
        返回成功的jsoin
        :param type: 类型 自定义数据或者
        :return:  json格式
        """

        if type:
            error = data
        else:
            error = {'status': 'success', 'errmsg': errmsg, 'data': data}

        json_str = json.dumps(error, ensure_ascii=False)
        # print(json_str)
        SendInfoToWebWithCallback(self.pSession, self.callback, json_str)

    def mx_export(self, pData, fileName):
        """
        导出浏览器窗口下载
        :param pData: 数据bytes
        :param fileName: 文件名称
        :return:
        """
        return SendInfoToWebExport(self.pSession, pData, fileName)

    def CheckError(self, nRet, error):
        """
        检查数据库句柄错误信息并返回错误
        :param nRet:
        :param error:
        :return:
        """
        if (int(nRet) != 0):
            self.mx_error(error)

    @staticmethod
    def array_search(Propertys, value):
        """
        在字典中查找指定的值并返回对应的key
        :param Propertys:
        :param value:
        :return:
        """
        return list(Propertys.keys())[list(Propertys.values()).index(value)]

    @staticmethod
    def Close_Handle(handle):
        """
        关闭句柄
        :param handle:
        :return:
        """
        pass
        # handle.closeHandle()

    @staticmethod
    def array_column(data, name, value):
        """
        将列表转成字段根据字典中key
        :param data:  列表
        :param name:  转成的字典的key
        :param value: 转成字典的value
        :return: 字典
        """
        tmp = {}
        for val in data:
            tmp[val[name]] = val[value]

        return tmp

    @staticmethod
    def array_multisort(result, name, reverse_):
        """
        字典按照key排序
        :param result:  字典
        :return: 排序后的字典
        """
        result.sort(key=lambda obj: (obj.get(name)), reverse=reverse_)

    @staticmethod
    def time2Units(time):
        """
        将时间按照汉字显示
        :param time: 需要转换的时间
        :return: 汉字时间字符串
        """
        year = math.floor(time / 60 / 60 / 24 / 365)
        time -= year * 60 * 60 * 24 * 365
        month = math.floor(time / 60 / 60 / 24 / 30)
        time -= month * 60 * 60 * 24 * 30
        day = math.floor(time / 60 / 60 / 24)
        time -= day * 60 * 60 * 24
        hour = math.floor(time / 60 / 60)
        time -= hour * 60 * 60
        minute = math.floor(time / 60)
        time -= minute * 60
        second = time
        str_ = ''
        unitArr = {'年': year, '个月': month, '天': day,
                   '小时': hour, '分钟': minute, '秒': second}
        for cn, u in unitArr.items():
            if u > 0:
                str_ += str(u) + cn

        return str_

    def mx_checkerror(self, nRet, error):
        """
        判断错误
        :param nRet: 错误值
        :param error: 错误信息
        :return:
        """
        if (int(nRet) != 0):
            self.mx_error(error)
            return False
        return True
