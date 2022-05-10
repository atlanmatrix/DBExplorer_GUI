# -*- coding: utf_8 -*-
# @Create   : 2021/7/22 16:23
# @Author   : yh
# @Remark   : 云智慧服务注册
import json
import logging
import os
import time
import sys
import configparser
import re

from dubbo.client import NacosRegister, DubboClient
from nacos import NacosClient
from mx_log import setup_log
setup_log()
try:
    from jkyweb.controller.customer.yunSmart.Conf import dev as conf
    from jkyweb.module.public.TreeModel import TreeModel
except ImportError:
    from jkyweb.controller.yunSmart.Conf import dev as conf
    from jkyweb.module.TreeModel import TreeModel


class NacosService:

    def __init__(self):
        self.db = TreeModel()
        self.nc = NacosRegister(hosts=conf['NACOS_HOST'], namespace=conf['NACOS_NAMESPACE'],
                                namespace_id=conf['NACOS_NAMESPACE'], username=conf['NACOS_USER'],
                                group_name=conf['NACOS_GROUP_NAME'], password=conf['NACOS_PWD'])
        self.nacos_client = NacosClient(conf['NACOS_HOST'], namespace=conf['NACOS_NAMESPACE'],
                                        username=conf['NACOS_USER'], password=conf['NACOS_PWD'])
        self.dubbo_client = DubboClient('com.cloudwise.douc.facade.DataDubboFacade', nacos_register=self.nc,
                                        dubbo_version=conf['NACOS_DUBBO_VERSION'], version=conf['NACOS_VERSION'])

    def authority_dict(self, **kwargs) -> dict:
        """
        kwargs参数：
            renew：是否覆盖原值
            moduleCode：模块编码，默认：130
            moduleName：模块名称，默认：基础监控
            routeId：路由id，默认：doim

        从数据库获取菜单权限数据
        """

        self.db.open('Config', 'UserRight', host=conf['DB_HOST'], port=conf['DB_PORT'], file='base')
        # 获取需要隐藏的权限
        try:
            hide_dict = {hide: 1 for hide in self.db.fetchone_value('hide').split(';')}
        except AssertionError:
            hide_dict = dict()

        # 构造基础字典数据
        result = {
            'renew': kwargs['renew'] if kwargs.get('renew') else 'false',
            'moduleCode': kwargs['module_code'] if kwargs.get('module_code') else '130',
            'moduleName': kwargs['module_name'] if kwargs.get('module_name') else '基础监控',
            'routeId': kwargs['routeId'] if kwargs.get('routeId') else 'doim',
            'menus': list()
        }

        # 递归获取权限数据
        def recursion(path, parent=''):
            sub_keys = self.db.open('Config', path, host=conf['DB_HOST'], port=conf['DB_PORT'], file='base').sub_keys()
            if sub_keys:
                for sub_key in sub_keys:
                    if not sub_key.startswith('MODUL_'):  # 只查询MODUL_开头的子键
                        continue
                    temp = dict()
                    temp['name'] = self.db.open('Config', path + '\\' + sub_key, host=conf['DB_HOST'],
                                                port=conf['DB_PORT'], file='base').fetchone_value('Label')
                    temp['code'] = self.db.fetchone_value('ID')
                    if temp.get('code') == '300101' or hide_dict.get(temp.get('code')):  # 跳过用户权限，不注册用户权限
                        continue
                    if parent:
                        temp['parentCode'] = parent
                    temp['type'] = 1
                    temp['description'] = ''
                    temp['funcUrlList'] = list()
                    result['menus'].append(temp)
                    recursion(path + '\\' + sub_key, temp.get('code'))

        recursion('UserRight')
        return result

    def business_data(self):
        """
        从数据库获取所有设备，并组成数据列表
        """
        logging.info('%s开始从数据库获取所有设备信息%s' % ('-' * 10, '-' * 10))
        business_data = list()
        ccu_list = self.db.open('Co', 'Co_1\\CCUList', file='master').sub_keys()
        for ccu in ccu_list:

            sd_dict = self.db.open(ccu, "1.SD", file="ccubase").sub_items(prop_list=["mxparent", "mxlabel", "isdel"])
            for sd_k, sd_v in sd_dict.items():
                if not sd_v.get("mxlabel"):  # 对于没有label的设备，不予同步
                    continue

                if not sd_v.get("isdel") or sd_v["isdel"] == 0:  # 筛选未删除的设备
                    business_data.append({
                        "code": ccu + "." + sd_k,
                        "name": sd_v["mxlabel"],
                        "description": sd_k,
                        "parentCode": ccu + "." + sd_v["mxparent"] if sd_v.get("mxparent") else ""
                    })

            sg_dict = self.db.open(ccu, "1.SG", file="ccubase").sub_items(prop_list=["mxparent", "mxlabel", "isdel"])
            for sg_k, sg_v in sg_dict.items():
                if not sg_v.get("isdel") or sg_v["isdel"] == 0:
                    business_data.append({
                        "code": ccu + "." + sg_k,
                        "name": sg_v["mxlabel"] if sg_v.get("mxlabel") else "null",
                        "description": sg_k,
                        "parentCode": ccu + "." + sg_v["mxparent"] if sg_v.get("mxparent") else ""
                    })

            ts_dict = self.db.open(ccu, "1.TS", file="ccubase").sub_items(prop_list=["mxlabel"])
            for ts_k, ts_v in ts_dict.items():
                business_data.append({
                    "code": ccu + "." + ts_k,
                    "name": ts_v["mxlabel"] if ts_v.get("mxlabel") else "null",
                    "description": ts_k,
                    "parentCode": ''
                })
        return business_data

    def auth_conf_add(self):
        """
        添加doim的权限配置信息到nacos
        """
        logging.info('%s开始添加功能权限信息到nacos%s' % ('-' * 10, '-' * 10))
        state = self.nacos_client.publish_config(conf['DOIM_AUTH_CONF_NAME'], conf['DOIM_AUTH_CONF_GROUP'],
                                                 json.dumps(self.authority_dict(), ensure_ascii=False))
        if state is True:
            logging.info('注册权限信息到nacos成功！')
        else:
            logging.error('注册权限信息到nacos失败！')

    def model_delete(self):
        """
        模块删除
        :return:
        """
        logging.info('%s开始删除旧的数据<模块>%s' % ('-' * 10, '-' * 10))
        data = {
            "dataType": "basicMonitor"
        }

        try:
            result = json.loads(self.dubbo_client.invoke('deleteMultiType', json.dumps(data)))
        except ValueError:
            logging.error('删除数据<模块>失败: 发送删除请求失败')
            raise ValueError
        if result.get('code') == '100000':
            logging.info('删除数据<模块>成功')
        else:
            logging.error('删除数据<模块>失败：%s' % str(result))

    def model_add(self):
        """
        模块注册
        注册基础监控模块到douc
        """
        logging.info('%s开始添加数据<模块>到DOUC%s' % ('-' * 10, '-' * 10))
        data = {
            "typeConfig": [
                {
                    "dataType": "basicMonitor",
                    "dataTypeName": "基础监控",
                    "isMaintenance": 1,
                    "isRead": 1,
                    "modelType": 2  # 1 代表列表模型，2 代表树形模型
                }
            ]
        }
        try:
            response = self.dubbo_client.invoke('initMultiTypeData', json.dumps(data))
            result = json.loads(response)
        except ValueError:
            logging.error('注册模块到DOUC失败: 发送注册请求失败')
            raise ValueError
        if result.get('code') == '100000':
            logging.info('注册模块到DOUC成功')
        else:
            logging.error('模块注册到DOUC失败：%s' % str(result))

    def device_list(self):
        """
        鉴权admin用户，获取所有设备列表
        """
        logging.info('%s开始获取当前已注册的数据<信息>%s' % ('-'*10, '-'*10))
        data = {
            'accountId': '110',
            'userId': '2',
            'dataType': 'basicMonitor'
        }
        try:
            result = json.loads(self.dubbo_client.invoke('getDataAuthInfo', json.dumps(data)))
        except ValueError:
            logging.error('获取当前已注册的数据<信息>失败')
            raise ValueError

        return [value['code'] for value in result['data'][
            'basicMonitor']] if result['data'].get('basicMonitor') else list()

    def delete(self, datas):
        """
        删除资源
        """
        logging.info('%s开始删除当前已注册的数据<信息>%s' % ('-'*10, '-'*10))
        data = {
            'accountId': '110',
            'datas': datas,
            'dataType': 'basicMonitor'
        }

        try:
            result = json.loads(self.dubbo_client.invoke('unregisterMultiTypeData', json.dumps(data)))
            if result.get('code') == '100000':
                logging.info('删除当前已注册的数据<信息>成功')
        except ValueError:
            logging.error('删除当前已注册的数据<信息>失败')
            raise ValueError

    def business_init(self):
        """
        业务数据资源初始化
        """
        logging.info('%s开始添加数据<信息>到DOUC%s' % ('-' * 10, '-' * 10))
        device_list = self.device_list()
        if len(device_list) != 0:  # 没有设备时不执行删除
            self.delete(device_list)

        data = dict()
        data['accountId'] = '110'  # 租户id
        data['createUserId'] = '2'  # 创建用户id
        data['dataType'] = 'basicMonitor'  # 要注册到哪个模块
        data['dataItems'] = self.business_data()

        try:
            result = json.loads(self.dubbo_client.invoke('registerMultiTypeTreeData', json.dumps(data)))
        except ValueError:
            logging.error('添加数据<信息>: 发送注册请求失败')
            raise ValueError
        if result.get('code') == '100000':
            logging.info('添加数据<信息>到DOUC成功')
        else:
            logging.error('添加数据<信息>到DOUC失败：%s' % str(result))

    def update_db(self):
        """
        更新数据库，删除init参数
        """
        path = os.path.join(__file__.split('webexpress')[0], 'middle', 'Conf', 'middle.ini')
        
        config = configparser.ConfigParser()
        config.read(path)
        server_type = config.get('main', 'servertype')
        self.db.open('Config', 'ProcessWatcher\\%s\\CloudWise' % server_type, file='ccubase'
                     ).insert_item('Parameter', '../webexpress/python/StartCloudWise.py')

    def restart_process_watcher(self):
        """
        重启进程守护程序，应用去除init参数的状态
        """
        os.popen('systemctl restart ProcessWatcher')

    def send_heartbeat(self):
        """
        保持doim与nacos的心跳
        """
        metadata = {
            'name': 'doim'
        }
        while 1:
            self.nacos_client.send_heartbeat(conf['DOIM_INSTANCE_NAME'], conf['DOIM_IP'], conf['DOIM_PORT'],
                                             cluster_name=conf['DOIM_CLUSTER_NAME'], metadata=metadata)
            time.sleep(5)

    def kafka_conf_write(self):
        """
        nacos中kafka数据写入
        :return:
        """
        from jkyweb.controller.customer.yunSmart.Conf import dev
        nacos = self.nacos_client
        read_nacos = nacos.get_config('commons.properties', 'commons')
        ret = re.findall(r'([^, ]+)', re.search(r'kafkaBrokerServers=(.*)\n', read_nacos).groups()[0])
        # 修改conf.py
        conf_path = os.path.join(__file__.split('webexpress')[0],
                                 'webexpress/python/jkyweb/controller/customer/yunSmart/Conf.py')
        conf_py = ""
        with open(conf_path, 'r+', encoding='utf-8') as f:
            for line in f.readlines():
                if line.find("CMDB_KAFKA_HOST") != -1:
                    line = "    'CMDB_KAFKA_HOST': %s" % (ret,) + ',\n'
                conf_py += line
        with open(conf_path, 'w', encoding='utf-8') as f:
            f.writelines(conf_py)
        # 修改dodb_conf.txt
        dodb_conf_path = os.path.join(__file__.split('webexpress')[0],
                                      'webexpress/python/jkyweb/controller/customer/yunSmart/dodb_conf.txt')
        data = ""
        with open(dodb_conf_path, 'r+', encoding='utf-8') as f:
            for line in f.readlines():
                if "#" not in line and "[" in line and "]" in line:
                    split_read = line.split(",", 1)[0]
                    line = rf"{split_read},{ret}" + "\n"
                data += line
        with open(dodb_conf_path, 'w', encoding='utf-8') as f:
            f.writelines(data)


if __name__ == '__main__':
    logging.info('%s开始进行CloudWise融合版数据注册%s' % ('-'*10, '-'*10))
    nacos = NacosService()
    nacos.auth_conf_add()
    print(sys.argv)
    if len(sys.argv) == 2 and sys.argv[1] == 'init':
        try:
            nacos.model_delete()
            nacos.model_add()
        except ValueError:
            nacos.model_add()
        nacos.business_init()
        nacos.update_db()
        nacos.restart_process_watcher()
        nacos.kafka_conf_write()
    nacos.send_heartbeat()
