# -*- coding: utf_8 -*-
# @Author:wl
# @Time:2021/4/18 
# @Remark:云智慧DODB脚本

import os
import re
import shutil
import configparser
import platform
import chardet
import time

try:
    from jkyweb.module.public.TreeModel import *
except:
    from jkyweb.module.TreeModel import *

#from jkyweb.module.TreeModel import *

# ToUinoPerformanceData.properties配置项
# m_prop = {
#                     "Message.middle":"1",
#                     "Kafka.URL":"10.161.68.117:9092,10.161.68.118:9092",
#                     "ActiveMQ.PerformanceData.switch":"0",
#                     "ActiveMQ.AlertData.switch":"1",
#                     "db.host":"192.168.62.35",
#                     "db.port":"8123",
#                     "ccu.db.host":"192.168.2.36"
#                 }

# ConfigParser 区分大小写问题
class myconf(configparser.ConfigParser):
    def __init__(self,defaults=None):
        configparser.ConfigParser.__init__(self,defaults=None)

    def optionxform(self, optionstr):
        return optionstr

class HandleIni:
    '''
    处理Ini文件的类
    '''


    def __init__(self,path,section,option,conding_format,value=None):
        self.path = path
        self.section = section
        self.option = option
        self.value = value
        self.conding_format = conding_format

    def query_all_sections(self):
        '''
        获取所有ini文件的section
        :return:
        '''
        pass


    def query_section_option(self):
        '''
        得到section中option的值
        :return:
        '''
        cfp = myconf()
        try:
            cfp.read(self.path,encoding=self.conding_format)
        except:
            cfp.read(self.path, encoding="utf-8-sig")

        res = cfp.get(self.section, self.option)

        return res

    def modify_content(self):
        '''
        修改或添加指定节点下指定option的值
        :return:
        '''
        print(self.path,self.section,self.option,self.value)
        cfp = myconf()
        try:
            cfp.read(self.path, encoding=self.conding_format)
        except:
            cfp.read(self.path, encoding="utf-8-sig")

        cfp.set(self.section, self.option, self.value)
        # 对configparser对象执行的一些修改操作，必须重新写回到文件才可生效
        print(self.conding_format)
        cfp.write(open(self.path, "w+",encoding=self.conding_format))

    def insert_section_and_option(self,section,option,value):
        '''
        添加section以及section指定节点下指定option的值
        :return:
        '''
        cfp = myconf()
        try:
            cfp.read(self.path, encoding=self.conding_format)
        except:
            cfp.read(self.path, encoding="utf-8-sig")

        print(cfp.has_section(section),111111111111)
        if not cfp.has_section(section):
            cfp.add_section(section)
            cfp.set(section, option, value)
            cfp.write(open(self.path, 'w+'))

class Properties:
    '''
        处理properties文件的类
    '''
    def __init__(self,file_name):
        self.file_name = file_name
        self.properties = dict()

        try:
            with open(self.file_name, 'r',encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line.find('=') > 0 and not line.startswith('#'):
                        strs = line.split('=')
                        self.properties[strs[0].strip()] = strs[1].strip()
        except Exception as e:
            raise e

    def has_key(self,key):
        return key in self.properties

    def get(self, key, default_value=''):
        if key in self.properties:
            return self.properties[key]

        return default_value

    # 在properties文件末尾中插入key,value
    def insert(self,key,value):
        try:
            with open(self.file_name,"a",encoding="utf-8") as wf:
                wf.write(f"{key} = {value}\n")

        except:
            with open(self.file_name, "a", encoding="gbk") as wf:
                wf.write(f"{key} = {value}\n")

        print(f"properties文件末尾中插入{key}={value}成功！！！")

    # properties文件中更新指定key的value值
    def update(self,key,new_value):
        value = self.get(key)
        print(value,"value")
        original_content = f"{key} = {value}\n"
        update_content = f"{key} = {new_value}\n"
        replace_property(self.file_name,original_content,update_content)

def write_func(content, path, mode="a+"):
    '''
    文件写入操作
    :param content:
    :param path:
    :param mode:
    :return:
    '''
    try:
        with open(path, mode, encoding="utf-8") as wf:
            wf.write(content)
    except FileNotFoundError:
        pass

def replace_property(file_name,original_content,update_content):
    '''
    :param file_name:原文件路径
    :param original_content: 需要更新的内容
    :param update_content: 更新内容
    :return:
    '''
    prefix = file_name.rsplit(".", 1)[0]
    suffix = file_name.rsplit(".", 1)[1]
    bak_path = f"{prefix}_bak.{suffix}"
    #print(bak_path)
    shutil.move(file_name,bak_path)
    try:
        with open(bak_path,"r",encoding="utf-8") as rf:
            lines = rf.readlines()
            for line in lines:
                if re.search(original_content,line):
                    line = line.replace(original_content,update_content)
                write_func(line, file_name)
    except:
        pass

    os.remove(bak_path)

# 检查文件编码格式
def check_codeing_format(file_path):
    with open(file_path,"rb") as f:
        data = f.read()
    if data:
        result = chardet.detect(data)
        codeing_formata = result.get("encoding").lower()
    else:
       codeing_formata = "utf-8"

    return codeing_formata

def modify_conf_file(data_ini,path_ini):
    '''
    修改ini文件
    :param data_ini:传参示例
        data_ini = {
            "main": {
                "OEM": "云智慧",
                "licenseCheckType": "1",
                "who": "1"
            },
            "safe": {
                "checktoken": "0",
                "checkverifycode": "0"
            }
        }
    :param path_ini:ini文件路径
    :return:
    '''
    conding_format = check_codeing_format(path_ini)

    if "TSConfig.ini" in path_ini:
        for section, content in data_ini.items():
            for option, value in content.items():
                handle_ini = HandleIni(path_ini, section, option, conding_format,value=value)
                handle_ini.modify_content()
    else:
        for section, content in data_ini.items():
            for option, value in content.items():
                handle_ini = HandleIni(path_ini, section, option, conding_format,value=value)
                handle_ini.insert_section_and_option(section,option,value)


    print(f"{path_ini}文件适配完成！！！")

# 管理服务的程序
def manage_services(flag = True):
    '''
    管理服务的命令
    :param cmd:命令
    :param flag:启动和关闭脚本的标识,flag = True默认执行启动脚本的命令
    :return:
    '''
    sys = platform.system()
    if sys == "Windows":
        if flag:
            os.system("net restart CreCloud_Process_Controller")
            os.system("net restart CreCloud_Task_Server")

        else:
            os.system("net restart CreCloud_Process_Controller")
            os.system("net restart CreCloud_Task_Server")

    elif sys == "Linux":
        if flag:
            print("restart service!!!!")
            # 脚本开启
            os.system("systemctl stop ProcessWatcher.service")
            time.sleep(2)
            os.system("systemctl stop TSManager.service")
            time.sleep(2)
            os.system("systemctl start ProcessWatcher.service")
            time.sleep(2)
            os.system("systemctl start TSManager.service")

        else:
            # 脚本关闭
            os.system("systemctl stop ProcessWatcher.service")
            time.sleep(2)
            os.system("systemctl stop TSManager.service")
            time.sleep(2)
            os.system("systemctl start ProcessWatcher.service")
            time.sleep(2)
            os.system("systemctl start TSManager.service")

# ProcessWatcher下插入ToUinoPerformanceData子键
def insert_db(db_host,servertype,name,Parameter,runpath="",WatchDll="",WatchFunc="",WatchStopThreadFunc=""):

    db = TreeModel()
    # 获取servertype下的子键
    #lst_sub_key = db.open("Config",sub_key=f"ProcessWatcher\\{servertype}").sub_keys()
    lst_sub_key = db.open("Config", sub_key=f"ProcessWatcher\\{servertype}",host=db_host, file='ccubase').sub_keys()

    key = "ToUinoPerformanceData"
    print(servertype)
    if key not in lst_sub_key:
        db.open("Config",sub_key=f"ProcessWatcher\\{servertype}",host=db_host, file='ccubase').insert_sub_key(sub_key=key)

    # 插入属性
    db.open("Config",sub_key=f"ProcessWatcher\\{servertype}\\{key}",host=db_host, file='ccubase').insert_items([("MaxMemory",0),("Name",name),("Parameter",Parameter),("RestartTime",""),
                                                                                  ("RunPath",runpath),("WatchDll",WatchDll),("WatchFunc",WatchFunc),
                                                                                  ("WatchStopThreadFunc",WatchStopThreadFunc)
                                                                                  ])
    print("插入数据成功！！！")

# 删除ToUinoPerformanceData子键
def del_ToUinoPerformanceData(db_host,servertype,sub_key):
    db = TreeModel()
    db.open("Config", sub_key=f"ProcessWatcher\\{servertype}",host=db_host,file="ccubase").delete(sub_key)
    print("删除ToUinoPerformanceData子键成功！！！")

def print_menu():
    print('''
            =========================================
                    dodb功能菜单
            1.脚本启动程序
                a).修改TSConfig.ini文件
                b).修改runalert.ini文件
                c).启动ToUinoPerformanceData程序
                d).重启ProcessWatcher、TSManager服务
                
            2.脚本关闭程序步骤如下
                a).停止ToUinoPerformanceData程序
                b).修改TSConfig.ini文件
                c).修改runalert.ini文件
                d).重启ProcessWatcher、TSManager服务   
            q.退出
            =========================================
        ''')

def oper(db_host,TSConfig_ini,runalert_ini,prop_file,servertype,name,Parameter):
    while True:
        print_menu()
        option = input("请输入要执行的操作：")

        if option == "1":
            while True:
                print(
                    '''
                        TSConfig.ini修改内容如下：
                        [main]
                        ResultMode = 3

                        runalert.ini修改内容如下：
                        [eventmq]
                        cachemq = 1
                    '''
                )

                data_ts = {
                    "main":{
                        "ResultMode":"3"
                    }
                }
                data_runalert = {
                    "eventmq":{
                        "cachemq":"1"
                    }
                }
                while True:
                    flag_ini = input(f"请确定是否要修改{TSConfig_ini}和{runalert_ini}文件？(Y/N):")
                    if flag_ini == "Y":
                        modify_conf_file(data_ts,TSConfig_ini)
                        modify_conf_file(data_runalert, runalert_ini)
                        break


                # print(f"{prop_file}文件修改内容如下：\n{m_prop}")
                #
                # while True:
                #     flag_prop = input(f"请确定是否需要修改ToUinoPerformanceData.properties文件?(Y/N):")
                #     if flag_prop == "Y":
                #         for key,new_value in m_prop.items():
                #             parse = Properties(prop_file)
                #             parse.update(key,new_value)
                #         break
                # print(f"{prop_file}文件更新成功！！！")

                # 将ToUinoPerformanceData程序加到ProcessWatcher管理进程中

                while True:
                    flag_ToUino = input("请确定是否需要启动ToUinoPerformanceData程序？(Y/N):")
                    if flag_ToUino == "Y":
                        # 根据server_type类型，往数据库插入数据
                        insert_db(db_host,servertype, name, Parameter)
                        break

                while True:
                    flag_server = input("请确定是否需要启动ProcessWatcher、TSManager服务？(Y/N):")
                    if flag_server == "Y":
                        manage_services(flag=True)

                        break

                break

        elif option == "2":
            while True:
                while True:
                    flag_ToUino = input("请确定是否要停止ToUinoPerformanceData服务？(Y/N):")
                    if flag_ToUino == "Y":
                        del_ToUinoPerformanceData(db_host,servertype,"ToUinoPerformanceData")
                        break

                print(
                    '''
                        TSConfig.ini修改内容如下：
                        [main]
                        ResultMode = 1

                        runalert.ini修改内容如下：
                        [eventmq]
                        cachemq = 0
                    '''
                )


                data_ts = {
                    "main": {
                        "ResultMode": "1"
                    }
                }
                data_runalert = {
                    "eventmq": {
                        "cachemq": "0"
                    }
                }
                while True:
                    flag_ini = input(f"请确定是否要修改{TSConfig_ini}和{runalert_ini}文件？(Y/N):")
                    if flag_ini == "Y":
                        modify_conf_file(data_ts, TSConfig_ini)
                        modify_conf_file(data_runalert, runalert_ini)
                        break

                while True:
                    flag_server = input(f"请确定是否要是否需要启动ProcessWatcher、TSManager？(Y/N):")
                    if flag_server == "Y":
                        manage_services()

                        break

                break

        elif option == "q":
            print("退出")
            break

        else:
            print("输入的选项不合法，请重新输入！！！")

if __name__ == '__main__':
    abspath = os.path.abspath(__file__)
    server_path = abspath.rsplit("webexpress")[0]

    system = platform.system()
    db_host = input("请输入数据库ip(例：192.168.15.32):")
    if system == "Windows":
        TSConfig_ini = f"{server_path}bin\\conf\\TSConfig.ini"
        runalert_ini = f"{server_path}bin\\conf\\runalert.ini"
        middle_path = f"{server_path}middle\\conf\\middle.ini"
        conding_format = check_codeing_format(middle_path)
        prop_file = f"{server_path}bin\\ToUinoPerformanceData.properties"

        handle_ini = HandleIni(middle_path, "main", "servertype", conding_format)
        servertype = int(
            handle_ini.query_section_option())

        name = "../python/python.exe"
        Parameter = f"{os.getcwd()}\\dodb_script.py"
        print(Parameter)

    elif system == "Linux":
        TSConfig_ini = f"{server_path}bin/conf/TSConfig.ini"
        runalert_ini = f"{server_path}bin/conf/runalert.ini"
        middle_path = f"{server_path}middle/Conf/middle.ini"
        conding_format = check_codeing_format(middle_path)
        prop_file = f"{server_path}bin/ToUinoPerformanceData.properties"

        handle_ini = HandleIni(middle_path, "main", "servertype", conding_format)
        servertype = int(
            handle_ini.query_section_option())

        name = "ToUinoPerformanceData"
        Parameter = ""

    oper(db_host,TSConfig_ini, runalert_ini, prop_file, servertype, name, Parameter)