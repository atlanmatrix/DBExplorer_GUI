#import json
from mxsoft import *
from BSWork import *
import sys
import math

class Base(object):

    def __init__(self,pSession):
        nRet, callbackparam, param = SessionInit(pSession, False, False)
        nRet,postData = pSession.GetPostString()
        print(postData)
        print(callbackparam)
        print(param)
        self.param = param
        self.callback = callbackparam
        self._sHostName = '127.0.0.1'
        self._uPort = 8123
        self.pSession = pSession
        

    def mx_error(self,errmsg):
        """
        返回错误的json
        :param errmsg: 错误消息
        :return: json格式
        """
        error = {'status' : 'failed','errmsg' : errmsg}
       # error.encode('utf-8').strip()
        sys.stdout.flush()
        print(errmsg)
        print(error)
        json_str = json.dumps(error,ensure_ascii=False)

        SendInfoToWebWithCallback(self.pSession,self.callback,json_str)
        # if self.callback :
        #     str = self.callback + "(" + json.dumps(error) + ")"
        #     return str
        # else:
        #     return jsonify(error)

    def mx_success(self, errmsg, data,type=None):
        """
        返回成功的jsoin
        :param type: 类型 自定义数据或者
        :return:  json格式
        """

        if type:
            error = data
        else:
            error = {'status': 'success', 'errmsg': errmsg, 'data': data}

        json_str = json.dumps(error,ensure_ascii=False)
       # print(json_str)
        SendInfoToWebWithCallback(self.pSession, self.callback, json_str)
        # if self.callback:
        #     str = self.callback + "(" + json.dumps(error) + ")"
        #     return str
        # else:
        #     return jsonify(error)

    @staticmethod
    def Close_Handle(handle):
        """
        关闭句柄
        :param handle:
        :return:
        """
        handle.closeHandle()

    @staticmethod
    def array_column(data,name,value):
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
    def array_multisort(result,name,reverse_):
        """
        字典按照key排序
        :param result:  字典
        :return: 排序后的字典
        """
        result.sort(key=lambda obj: (obj.get(name)), reverse=reverse_)

    @staticmethod
    def time2Units(time):
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
        unitArr = {'年' : year, '个月' : month, '天' : day,
            '小时' : hour, '分钟' : minute, '秒' : second }
        for cn,u in unitArr.items():
            if u > 0 :
                str_ += str(u)+cn

        return str_
