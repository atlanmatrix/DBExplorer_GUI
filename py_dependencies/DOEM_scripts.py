# -*- coding: utf-8 -*-
# version 1.0
# author wl

import os
import time
import chardet
import platform
import configparser

# DODE 发送告警runalert.ini配置项
# data_runalert = {
#                     "cloudwise": {
#                         "send": "1",
#                         "url":"http://219.142.240.76:8899/api/v1/artemis/message/rest",
#                         "appkey":"36fb10a4-3f60-41dd-84b8-6993aba0fda2"
#                     }
#                 }

# ConfigParser 区分大小写问题
class Myconf(configparser.ConfigParser):
    def __init__(self,defaults=None):
        configparser.ConfigParser.__init__(self,defaults=None)

    def optionxform(self, optionstr):
        return optionstr

class HandleIni:

    def __init__(self,path,section,option,conding_format,value=None):
        self.path = path
        self.section = section
        self.option = option
        self.value = value
        self.conding_format = conding_format

    def query_section_option(self):
        '''
        得到section中option的值
        :return:
        '''
        cfp = configparser.ConfigParser()
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
        cfp = Myconf()
        try:
            cfp.read(self.path, encoding=self.conding_format)
        except:
            cfp.read(self.path, encoding="utf-8-sig")

        cfp.set(self.section, self.option, self.value)
        # 对configparser对象执行的一些修改操作，必须重新写回到文件才可生效
        cfp.write(open(self.path, "w+",encoding=self.conding_format))

    def insert_section_and_option(self,section,option,value):
        '''
        添加section以及section指定节点下指定option的值
        :return:
        '''
        cfp = Myconf()
        try:
            cfp.read(self.path, encoding=self.conding_format)
        except:
            cfp.read(self.path, encoding="utf-8-sig")

        if not cfp.has_section(section):
            cfp.add_section(section)
            cfp.set(section, option, value)
            cfp.write(open(self.path, 'w+'))

    def del_section_and_option(self):
        cfp = Myconf()
        try:
            cfp.read(self.path, encoding=self.conding_format)
        except:
            cfp.read(self.path, encoding="utf-8-sig")

        cfp.remove_section(self.section)
        cfp.write(open(self.path, 'w+'))

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

    for section, content in data_ini.items():
        for option, value in content.items():
            handle_ini = HandleIni(path_ini, section, option, conding_format, value=value)
            handle_ini.modify_content()

    print(f"{path_ini}文件适配完成！！！")

# 管理服务的程序
def manage_services(opt):
    '''
    管理服务的命令
    :return:
    '''
    sys = platform.system()
    if sys == "Windows":
        if opt == 1:
            print("stop ProcessWatcher service!!!!")
            os.system("net restart CreCloud_Process_Controller")
        elif opt == 3:
            print("restart ProcessWatcher service!!!!")
            os.system("net restart CreCloud_Task_Server")

    elif sys == "Linux":
        if opt == 1:
            print("stop ProcessWatcher service!!!!")
            os.system("systemctl stop ProcessWatcher.service")
            time.sleep(2)
        elif opt == 2:
            print("restart ProcessWatcher service!!!!")
            os.system("systemctl stop ProcessWatcher.service")
            time.sleep(2)
            os.system("systemctl start ProcessWatcher.service")
            time.sleep(2)

def print_menu():
    print('''
            =========================================
                    DOEM功能菜单
            1.推送告警过程
                a.停止ProcessWatcher服务
                b.runalert.ini配置文件增加云平台推送告警信息
                c.启动ProcessWatcher服务
                
            2.关闭推送告警
                a.runalert.ini配置文件
                b.启动ProcessWatcher服务
                
            q.退出
            =========================================
        ''')

def oper(runalert_ini):
    while True:
        print_menu()
        option = input("请输入要执行的操作：")

        if option == "1":

            while True:
                print("推送告警过程！！！")
                while True:
                    # 停止ProcessWatcher服务
                    flag_stop = input("请确定是否需要停止ProcessWatcher服务？(Y/N):")
                    if flag_stop == "Y":
                        manage_services(int(option))
                        break

                data_runalert = {
                    "cloudwise": {
                        "send": "1"
                    }
                }
                while True:
                    flag_runalert = input("请确定是否要推送告警？(Y/N):")
                    if flag_runalert == "Y":
                        modify_conf_file(data_runalert,runalert_ini)
                        break

                while True:
                    flag_conf = input("请确定是否要启动ProcessWatcher服务？(Y/N):")
                    if flag_conf == "Y":
                        manage_services(2)
                        break
                break

        elif option == "2":
            while True:
                print("关闭推送告警!!!")
                data_runalert = {
                    "cloudwise": {
                        "send": "0"
                    }
                }
                while True:
                    flag_runalert = input("请确定是否要关闭告警？(Y/N):")
                    if flag_runalert == "Y":
                        modify_conf_file(data_runalert,runalert_ini)
                        break

                while True:
                    flag_conf = input("请确定是否要启动ProcessWatcher服务？(Y/N):")
                    if flag_conf == "Y":
                        manage_services(int(option))
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

    sys = platform.system()
    if sys == "Windows":
        runalert_ini = f"{server_path}bin\\conf\\runalert.ini"

    elif sys == "Linux":
        runalert_ini = f"{server_path}bin/conf/runalert.ini"

    oper(runalert_ini)
