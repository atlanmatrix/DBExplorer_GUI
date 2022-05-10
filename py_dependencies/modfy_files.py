# -*- coding: utf_8 -*-
# @Author : wl
# @Time : 2021/4/30 14:30
# @Remark: 云智慧转换脚本(静态资源不加网关)

import os
import re
import sys
sys.path.append(f"{os.getcwd().rsplit('webexpress')[0]}webexpress{os.sep}python{os.sep}jkyweb")
import os
import time
import fnmatch
import shutil
import configparser
import platform
import chardet
import threading
from multiprocessing import Process
from functools import lru_cache
try:
    from jkyweb.module.public.TreeModel import *
except ImportError:
    from jkyweb.module.TreeModel import *

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

    def write_content(self):
        '''
        ini文件中写入指定内容
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
        cfp.write(open(self.path, "w+"))

# 构造数据对象
data = {
    "'/bundles/": "'/doim/bundles/",
    '"/bundles/': '"/doim/bundles/',
    '"/css/': '"/doim/css/',
    "'/css/": "'/doim/css/",
    "'/js/": "'/doim/js/",
    '"/js/': '"/doim/js/',
    "'/images/": "'/doim/images/",
    '"/images/': '"/doim/images/',
    '"/client/': '"/doim/client/',
    "'/client/": "'/doim/client/",
    '"/3dht/': '"/doim/3dht/',
    "'/3dht/": "'/doim/3dht/",
    '"/fonts/': '"/doim/fonts/',
    "'/fonts/": "'/doim/fonts/",
    '"/login_files/': '"/doim/login_files/',
    "'/login_files/": "'/doim/login_files/",
    '"/MxsoftBigData/': '"/doim/MxsoftBigData/',
    "'/MxsoftBigData/": "'/doim/MxsoftBigData/",
    '"/panel/': '"/doim/panel/',
    "'/panel/": "'/doim/panel/",
    '"/port/': '"/doim/port/',
    "'/port/": "'/doim/port/",
    '"/simulation/': '"/doim/simulation/',
    "'/simulation/": "'/doim/simulation/",
    '"/svg/': '"/doim/svg/',
    "'/svg/": "'/doim/svg/",
    '"/symbols/': '"/doim/symbols/',
    "'/symbols/": "'/doim/symbols/",
    "url\(/images/":"url(/doim/images/",
    '''"'\+Entities\[k\]\.Icon\+'"''':'''"/doim'+Entities[k].Icon+'"''',
    'post\("/': 'post("/gateway/doim/',
    "post\('/": "post('/gateway/doim/",
    "\$\.getJSON\('/" : "$.getJSON('/gateway/doim/",
    '\$\.getJSON\("/' : 'getJSON("/gateway/doim/',
    'location.href="/':'location.href = "/doim/',
    "location.href='/":"location.href = '/doim/",
    'location.href = "/':'location.href = "/doim/',
    "location.href = '/":"location.href = '/doim/",
    #"var twourl = '/": "var twourl = '/gateway/doim/",
    #'var twourl = "/': 'var twourl = "/gateway/doim/',
    #"var url = '/": "var url = '/gateway/doim/",
    #'var url = "/': 'var url = "/gateway/doim/',
    # 'src="/':'src="/gateway/doim/',
    # "src='/":"src='/gateway/doim/",
    # 'src = "/':'src = "/gateway/doim/',
    # "src = '/":"src = '/gateway/doim/",
    #'location.href = \("/':'location.href = "(/gateway/doim/',
    #"location.href = \('/":"location.href = '(/gateway/doim/",

    # html适配规则
    "<!--master_ty_sys_begin-->":"<!--master_ty_sys_begin",
    "<!--master_ty_sys_end-->":"master_ty_sys_end-->",
    "<!--master_ty_sys_begin_xui-->":"<!--master_ty_sys_begin_xui",
    "<!--master_ty_sys_end_xui-->":"master_ty_sys_end_xui-->",

    # css适配规则
    "/\*master_ty_sys_begin\*/":"/*master_ty_sys_begin",
    "/\*master_ty_sys_end\*/":"master_ty_sys_end*/",
    "/\*master_ty_sys_begin_xui\*/":"/*master_ty_sys_begin_xui",
    "/\*master_ty_sys_end_xui\*/":"master_ty_sys_end_xui*/",
    '/login.html':'/gateway/doim/login.html'
}

# 判断文件内容是否为空的函数
def check_file_size(file_path:str):
    flag = False
    try:
        size = os.path.getsize(file_path)
        if size == 0:
            flag = True
    except:
        pass

    return flag

# 检查文件内容是否改变的标识
# 检查文件内容是否改变的标识
def check_file_content(file_path: str):
    '''
    :param file_path:
    :return:
    '''
    flag_file_change = False
    try:
        with open(file_path, 'r', encoding="utf-8") as rf:
            lines = rf.read()
    except:
        with open(file_path, 'r', encoding="gbk") as rf:
            lines = rf.read()

    if re.search("/gateway/doim/", lines) or re.search("/doim/", lines):
        flag_file_change = True

    return flag_file_change

def all_files(root, patterns='*', single_level=False, yield_folder=False):
    # 将模式从字符串中取出放入列表中
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folder:
            files.extend(subdirs)
        files.sort()
        for fname in files:
            for pt in patterns:
                if fnmatch.fnmatch(fname, pt):
                    yield os.path.join(path, fname)
                    break
        if single_level:
            break

def open_file(file):
    '''
    打开文件操作
    :param file:
    :return:
    '''
    try:
        with open(file, 'r', encoding="utf-8") as rf:
            lines = rf.readlines()
    except:
        with open(file, 'r',encoding="gbk") as rf:
            lines = rf.readlines()
    return lines

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

def bak_file(old_path):
    '''
    备份文件操作
    :param old_path:
    :param new_path:
    :return:
    '''
    prefix = old_path.rsplit(".", 1)[0]
    suffix = old_path.rsplit(".", 1)[1]
    new_path = f"{prefix}_bak.{suffix}"

    return new_path

def query_str_time():
    local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    return local_time

def insert_mxishide_label(db_host,main_key,sub_key):
    db = TreeModel()
    #main_key = "EntityTemplate"
    db.open(main_key,sub_key=sub_key,host=db_host,file="base").insert_item("mxishide","1")

def query_gis(db_host,tp,main_key):
    db = TreeModel()
    res = list()
    # 递归获取权限数据i
    @lru_cache(maxsize=1024)
    def recursion(path):
        try:
            sub_keys = db.open(main_key, path,host=db_host,file="base").sub_keys()
        except:
            return
        if sub_keys:
            for sub_key in sub_keys:
                if sub_key == '_gis':
                    print("path===========>",path + '\\_gis')
                    res.append(path + '\\_gis')

                elif sub_key == "_gisIcon":
                    res.append(path + '\\_gisIcon')

                else:
                    recursion(path + '\\' + sub_key)

    recursion(tp)
    return res

def remove_header_file(file_path):
    '''
    去头文件替换
    :return:
    '''
    lst_rhb_files = list(all_files(file_path, '*.css_rhb;*.js_rhb;*.png_rhb;*.json_rhb'))
    print("lst_rhb_files", lst_rhb_files)
    lst_standard_file = [path.rsplit("_rhb", 1)[0] for path in lst_rhb_files]
    print("lst_standard_file", lst_standard_file)

    # 删除原始文件
    # for standard_file in lst_standard_file:
    #     print("standard_file",standard_file)
    #     if os.path.exists(standard_file):
    #         os.remove(standard_file)
    #
    # print("原始头文件删除成功！！！")
    # # 重命名融合版名字
    print("lst_standard_file",lst_standard_file)
    for rhb_file, standard_file in zip(lst_rhb_files, lst_standard_file):
        #shutil.move(rhb_file, standard_file)
        shutil.copyfile(rhb_file, standard_file)

    print("重命名融合版本文件成功！！！")

def front_end_file(file_path):
    '''
    前端文件替换规则检验
    :param file_path:
    :return:
    '''
    #if not check_file_content(file_path):
    lines = open_file(file_path)
    suffix = file_path.rsplit(".", 1)[-1]

    if suffix == "css":
        for line in lines:
            if "/*yzh_rhb_ty_sys_begin*/\n" in line:
                pass
            elif "/*yzh_rhb_ty_sys_end*/" in line or "/*yzh_rhb_ty_sys_end*/\n" in line:
                pass

            elif "/*yzh_rhb_ty_sys_begin_xui*/\n" in line:
                pass

            elif "/*yzh_rhb_ty_sys_end_xui*/" in line or "/*yzh_rhb_ty_sys_end_xui*/\n" in line:
                pass

            elif "/*yzh_rhb_ty_sys_begin\n" in line:
                line = line.replace(line,"/*yzh_rhb_ty_sys_begin*/\n")

            elif "/*yzh_rhb_ty_sys_begin_xui\n" in line:
                line = line.replace(line,"/*yzh_rhb_ty_sys_begin_xui*/\n")


            elif  "yzh_rhb_ty_sys_end*/\n" in line:
                line = line.replace(line, "/*yzh_rhb_ty_sys_end*/\n")

            elif "yzh_rhb_ty_sys_end_xui*/\n" in line:
                line = line.replace(line, "/*yzh_rhb_ty_sys_end_xui*/\n")

            elif "yzh_rhb_ty_sys_end_xui*/\n" in line:
                line = line.replace(line, "/*yzh_rhb_ty_sys_end_xui*/\n")

            elif '$.post("/gateway/doim' in line or "$.post('/gateway/doim" in line:
                pass

            else:
                for k in data:
                    if re.search(k, line):
                        if k == "/\*master_ty_sys_begin\*/":
                            line = line.replace("/*master_ty_sys_begin*/", data[k])

                        elif k == "/\*master_ty_sys_end\*/":
                            line = line.replace("/*master_ty_sys_end*/", data[k])

                        if k == "/\*master_ty_sys_begin_xui\*/":
                            line = line.replace("/*master_ty_sys_begin_xui*/", data[k])

                        elif k == "/\*master_ty_sys_end_xui\*/":
                            line = line.replace("/*master_ty_sys_end_xui*/", data[k])

                        elif k == "url\(/images/":
                            line = line.replace("url(/images/", data[k])

                        else:
                            line = line.replace(k, data[k])

                        break

            write_func(line, bak_file(file_path))

    elif suffix == "js":
        for line in lines:
            if "/*yzh_rhb_ty_sys_begin*/\n" in line:
                pass

            elif "/*yzh_rhb_ty_sys_begin_xui*/\n" in line:
                pass

            elif "/*yzh_rhb_ty_sys_end*/" in line or "/*yzh_rhb_ty_sys_end*/\n" in line:
                pass

            elif "/*yzh_rhb_ty_sys_end_xui*/" in line or "/*yzh_rhb_ty_sys_end_xui*/\n" in line:
                pass

            elif '$.post("/gateway/doim' in line or "$.post('/gateway/doim" in line:
                pass

            elif '$.getJSON("/gateway/doim' in line or "$.getJSON('/gateway/doim" in line:
                pass

            elif "/*yzh_rhb_ty_sys_begin\n" in line:
                line = line.replace(line, "/*yzh_rhb_ty_sys_begin*/\n")

            elif "yzh_rhb_ty_sys_end*/\n" in line:
                line = line.replace(line, "/*yzh_rhb_ty_sys_end*/\n")

            elif "/*yzh_rhb_ty_sys_begin_xui\n" in line:
                line = line.replace(line, "/*yzh_rhb_ty_sys_begin_xui*/\n")


            elif "yzh_rhb_ty_sys_end_xui*/\n" in line:
                line = line.replace(line, "/*yzh_rhb_ty_sys_end_xui*/\n")

            elif '//master_ty_sys_begin\n' in line:
                line = line.replace(line,'/*master_ty_sys_begin\n')

            elif line == '//master_ty_sys_end' in line or '//master_ty_sys_end\n' in line:
                line = line.replace(line, 'master_ty_sys_end*/\n')

            elif '//master_ty_sys_begin_xui\n' in line:
                line = line.replace(line,'/*master_ty_sys_begin_xui\n')

            elif 'location.href = ("/gateway/doim/' in line:
                pass
            elif "location.href = ('/gateway/doim/" in line:
                pass

            elif 'location.href = ("/' in line:
                line = line.replace('location.href = ("/','location.href = ("/gateway/doim/')

            elif "location.href = ('/" in line:
                line = line.replace("location.href = ('/","location.href = ('/gateway/doim/")

            elif line == '//master_ty_sys_end_xui' or '//master_ty_sys_end_xui\n' in line:
                line = line.replace(line, 'master_ty_sys_end_xui*/\n')

            else:
                for k in data:
                    if re.search(k, line):
                        if k == 'post\("/':
                            line = line.replace('post("/', data[k])
                        elif k == "post\('/":
                            line = line.replace("post('/", data[k])

                        # elif k == 'getJSON\("/':
                        #     line = line.replace('getJSON("/', data[k])
                        #
                        # elif k == "getJSON\('/":
                        #     line = line.replace("getJSON('/", data[k])

                        elif k == 'location.href = \("/':
                            line = line.replace(k,data[k])

                        elif k == "location.href = \('/":
                            line = line.replace(k,data[k])

                        elif k == "url\(/images/":
                            line = line.replace("url(/images/", data[k])

                        elif k == '''"'\+Entities\[k\]\.Icon\+'"''':
                            line = line.replace('''"'+Entities[k].Icon+'"''', data[k])
                        else:
                            line = line.replace(k, data[k])
                        break

            write_func(line, bak_file(file_path))

    elif suffix == "html":

        for line in lines:
            if "<!--yzh_rhb_ty_sys_begin\n" in line:
                line = line.replace(line,"<!--yzh_rhb_ty_sys_begin-->\n")

            elif "yzh_rhb_ty_sys_end-->\n" in line:
                line = line.replace("yzh_rhb_ty_sys_end-->\n","<!--yzh_rhb_ty_sys_end-->\n")

            elif "<!--yzh_rhb_ty_sys_begin_xui\n" in line:
                line = line.replace(line,"<!--yzh_rhb_ty_sys_begin_xui-->\n")

            elif "yzh_rhb_ty_sys_end_xui-->\n" in line:
                line = line.replace(line,"<!--yzh_rhb_ty_sys_end_xui-->\n")

            elif "<!--yzh_rhb_ty_sys_begin-->\n" in line:
                pass

            elif "<!--yzh_rhb_ty_sys_begin_xui-->\n" in line:
                pass

            elif "<!--yzh_rhb_ty_sys_end-->\n" in line or "<!--yzh_rhb_ty_sys_end-->" in line:
                pass

            elif "<!--yzh_rhb_ty_sys_end_xui-->\n" in line or "<!--yzh_rhb_ty_sys_end_xui-->" in line:
                pass

            elif "/*yzh_rhb_ty_sys_begin*/\n" in line:
                pass

            elif "/*yzh_rhb_ty_sys_begin_xui*/\n" in line:
                pass

            elif "/*yzh_rhb_ty_sys_end*/" in line or "/*yzh_rhb_ty_sys_end*/\n" in line:
                pass

            elif "/*yzh_rhb_ty_sys_end_xui*/" in line or "/*yzh_rhb_ty_sys_end_xui*/\n" in line:
                pass

            elif '$.post("/gateway/doim' in line or "$.post('/gateway/doim" in line:
                pass

            elif '$.getJSON("/gateway/doim' in line or "$.getJSON('/gateway/doim" in line:
                pass

            elif "/*yzh_rhb_ty_sys_begin\n" in line:
                line = line.replace(line,"/*yzh_rhb_ty_sys_begin*/\n")

            elif "yzh_rhb_ty_sys_end*/\n" in line:
                line = line.replace(line, "/*yzh_rhb_ty_sys_end*/\n")

            elif "/*yzh_rhb_ty_sys_begin_xui\n" in line:
                line = line.replace(line,"/*yzh_rhb_ty_sys_begin_xui*/\n")


            elif "yzh_rhb_ty_sys_end_xui*/\n" in line:
                line = line.replace(line, "/*yzh_rhb_ty_sys_end_xui*/\n")

            elif '//master_ty_sys_begin\n' in line:
                line = line.replace(line, '/*master_ty_sys_begin\n')

            elif line == '//master_ty_sys_end' in line or '//master_ty_sys_end\n' in line:
                line = line.replace(line, 'master_ty_sys_end*/\n')

            elif '//master_ty_sys_begin_xui\n' in line:
                line = line.replace(line, '/*master_ty_sys_begin_xui\n')

            elif 'location.href = ("/gateway/doim/' in line:
                pass

            elif "location.href = ('/gateway/doim/" in line:

                pass

            elif 'location.href = ("/' in line:
                line = line.replace('location.href = ("/','location.href = ("/gateway/doim/')

            elif "location.href = ('/" in line:
                line = line.replace("location.href = ('/","location.href = ('/gateway/doim/")

            elif line == '//master_ty_sys_end_xui' or '//master_ty_sys_end_xui\n' in line:
                line = line.replace(line, 'master_ty_sys_end_xui*/\n')

            else:
                for k in data:
                    if re.search(k, line):
                        if k == 'post\("/':
                            line = line.replace('post("/', data[k])

                        elif k == "post\('/":
                            line = line.replace("post('/", data[k])

                        # elif k == 'getJSON\("/':
                        #     line = line.replace('getJSON("/', data[k])
                        #
                        # elif k == "getJSON\('/":
                        #     line = line.replace("getJSON('/", data[k])

                        elif k == "url\(/images/":
                            line = line.replace("url(/images/", data[k])

                        elif k == '''"'\+Entities\[k\]\.Icon\+'"''':
                            line = line.replace('''"'+Entities[k].Icon+'"''', data[k])

                        elif k == 'location.href = \("/':
                            line = line.replace(k, data[k])

                        elif k == "location.href = \('/":
                            line = line.replace(k, data[k])

                        else:
                            line = line.replace(k, data[k])
                        break

            write_func(line, bak_file(file_path))

    else:
        for line in lines:
            for k in data:
                if re.search(k, line):

                    if k == 'post\("/':
                        line = line.replace('post("/', data[k])
                    elif k == "post\('/":
                       line = line.replace("post('/", data[k])

                    elif k == "/\*yzh_rhb_ty_sys_begin":
                        line = line.replace("/*yzh_rhb_ty_sys_begin", data[k])
                    elif k == "yzh_rhb_ty_sys_end\*/":
                        line = line.replace("yzh_rhb_ty_sys_end*/", data[k])

                    elif k == "url\(/images/":
                        line = line.replace("url(/images/", data[k])
                    elif k == '''"'\+Entities\[k\]\.Icon\+'"''':
                        line = line.replace('''"'+Entities[k].Icon+'"''', data[k])
                    else:
                        line = line.replace(k, data[k])
                        print("line", line)
                    break

            write_func(line, bak_file(file_path))

    log_info = f"{file_path}文件修改成功!!!!!"

    return log_info

def replace_file(lst_files:list):
    '''
    修改前端文件
    :return:
    '''
    for file in lst_files:
        escape_file = '\\\\'.join(file.split('\\'))
        path, filename = os.path.split(escape_file)
        # 匹配前端文件路径中包含.的个数，不大于2个匹配
        lst_point = re.findall("\.", filename)

        if not check_file_content(file):

            if len(lst_point) < 2:
                if not check_file_size(escape_file):
                    log_info = front_end_file(escape_file)
                    print("log_info===================>", log_info)
                    # _bak文件,重命名
                    lst_bak = escape_file.rsplit(".")
                    lst_escape_bak = [f"{lst_bak[0]}_bak", lst_bak[-1]]
                    escape_bak = ".".join(lst_escape_bak)
                    os.remove(escape_file)
                    try:
                        os.rename(escape_bak, escape_file)
                    except:
                        continue


def modify_conf_file(middle_ini):
    '''
    修改ini文件
    :return:
    '''
    if not check_file_content(middle_ini):
        middle_data = {
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
        conding_format = check_codeing_format(middle_ini)
        for section, content in middle_data.items():
            for option, value in content.items():
                print(section, option, value)
                handle_ini = HandleIni(middle_ini, section, option, conding_format, value=value)
                handle_ini.write_content()

        print("middle.ini文件适配完成！！！")

def close_gis_db_label(db_host,main_key):
    '''
    关闭数据库gis组
    :return:
    '''
    db = TreeModel()
    lst_sub_key = db.open(main_key,"",host=db_host,file="base").sub_keys()
    print("lst_sub_key", lst_sub_key, len(lst_sub_key))
    lst_gis = []

    for sub_key in lst_sub_key:
        lst = query_gis(db_host,sub_key,main_key)
        lst_gis.extend(lst)

    print("lst_gis", lst_gis, len(lst_gis))

    # 隐藏_gis和_gisIcon属性
    if lst_gis:
        for gis in lst_gis:
             insert_mxishide_label(db_host,main_key,gis)

    print("隐藏_gis和_gisIcon属性成功！！！")

def print_menu():
    print('''
        =========================================
                云智慧单机版升级融合版功能菜单
        0.默认执行所有功能
        1.批量替换前端文件（*.html,*.js,*.css）
        2.修改middle.ini文件
        3.数据库组gis关闭及隐藏版本
        4.去头
        q.退出
        =========================================
    ''')

def split_list_average_n(origin_list, n):
    for i in range(0, len(origin_list), n):
        yield origin_list[i:i + n]

def worker(lst_files, func):
    if len(lst_files) < 8:
        replace_file(lst_files)

    else:
        interval = int(len(lst_files) // 8)
        for i in range(8):
            th = threading.Thread(target=func, args=(lst_files[interval*i:interval*(i+1)],))
            th.start()



def batch_replace_file(p):
    p.start()
    p.join()

def oper(db_host,lst_files, hdoc_path,middle_ini):
    while True:
        print_menu()
        option = input("请输入要执行的操作：")
        if option == "0":
            print("默认执行所有操作！！！")
            #batch_replace_file(lst_files, replace_file)
            p = Process(target=worker, args=(lst_files, replace_file))
            batch_replace_file(p)
            modify_conf_file(middle_ini)
            close_gis_db_label(db_host, "EntityTemplate")
            close_gis_db_label(db_host, "IndustryTemplate")
            remove_header_file(hdoc_path)

        elif option == "1":
            while True:
                print(f"前端路径{hdoc_path}文件替换规则如下:")
                print('''
                    1.所有文件夹bundles的路径（"/bundles/ 和 '/bundles/  改为 "/gateway/doim/bundles/）
                    2.所有文件夹css的路径（"/css/ 和 '/css/  改为 "/gateway/doim/css/）
                    3.所有文件夹js的路径（"/js/ 和 '/js/  改为 "/gateway/doim/js/）
                    4.所有文件夹images的路径（"/images/ 和 '/images/  改为 "/gateway/doim/images/）
                    5.所有文件夹client的路径（"/client/ 和 '/client/  改为 "/gateway/doim/client/）
                    6.所有文件夹3dht的路径（"/3dht/ 和 '/3dht/  改为 "/gateway/doim/3dht/）
                    7.所有文件夹fonts的路径（"/fonts/ 和 '/fonts/  改为 "/gateway/doim/fonts/）
                    8.所有文件夹login_files的路径（"/login_files/ 和 '/login_files/  改为 "/gateway/doim/login_files/）
                    9.所有文件夹MxsoftBigData的路径（"/MxsoftBigData/ 和 '/MxsoftBigData/  改为 "/gateway/doim/MxsoftBigData/）
                    10.所有文件夹panel的路径（"/panel/ 和 '/panel/  改为 "/gateway/doim/panel/）
                    11.所有文件夹port的路径（"/port/ 和 '/port/  改为 "/gateway/doim/port/）
                    12.所有文件夹simulation的路径（"/simulation/ 和 '/simulation/  改为 "/gateway/doim/simulation/）
                    13.所有文件夹svg的路径（"/svg/ 和 '/svg/  改为 "/gateway/doim/svg/）
                    14.所有文件夹symbols的路径（"/symbols/ 和 '/symbols/  改为 "/gateway/doim/symbols/）
                    15.所有文件的路径 （ background: url(images/  改为 background: url(/gateway/doim/images/）
                    16.所有文件的路径 （ .attr('src','/  改为  .attr('src','/gateway/doim/ ）
                    17.将Common.js以及html，及css文件中标准版代码注释掉，放开云智慧相关代码块
                    18.所有文件的路径 （ 'location.href="/'改为'location.href = "/gateway/doim/' ）
                    19.将登录页面路径'/login.html'替换为'/gateway/doim/login.html'
                ''')
                flag = input("请确定是否要批量替换前端文件？(Y/N):")
                if flag == "Y":
                    s_time = time.perf_counter()
                    #batch_replace_file(lst_files, replace_file)
                    p = Process(target=worker, args=(lst_files, replace_file))
                    batch_replace_file(p)
                    print("文件批量修改成功！！！！")
                    e_time = time.perf_counter()
                    print(f"程序耗时：{e_time - s_time}")
                    break

        elif option == "2":
            while True:
                print(
                    '''
                        修改内容如下：
                        [main]
                        OEM = 云智慧
                        licensechecktype = 1
                        who = 1
                         
                        [safe]
                        checktoken = 0
                        checkverifycode = 0
                    '''
                )
                flag = input(f"请确定是否要修改{middle_ini}文件？(Y/N):")
                if flag == "Y":
                    modify_conf_file(middle_ini)
                    break

        elif option == "3":
            while True:
                flag = input("请确定是否关闭gis组操作？(Y/N):")
                if flag == "Y":
                    start_time = time.time()
                    close_gis_db_label(db_host, "EntityTemplate")
                    close_gis_db_label(db_host, "IndustryTemplate")
                    end_time = time.time()
                    print("time:%d" % (end_time - start_time))
                    print("restart WebExpress services!!!")
                    os.system("systemctl stop WebExpress.service")
                    time.sleep(2)
                    os.system("systemctl start WebExpress.service")
                    time.sleep(2)
                    break

        elif option == "4":
            while True:
                flag = input("前端文件去头操作？(Y/N):")
                if flag == "Y":
                    remove_header_file(hdoc_path)
                    break

        elif option == "q":
            print("退出")
            break

        else:
            print("输入的选项不合法，请重新输入！！！")

if __name__ == '__main__':

    abspath = os.path.abspath(__file__)
    hdoc_path = abspath.split("python")[0] + "hdoc"
    sys = platform.system()
    db_host = input("请输入数据库ip:")
    if sys == "Windows":
        js_path = f"{hdoc_path}\js\Common.js"
        middle_ini = abspath.split("\\webexpress")[0]
        middle_ini = f"{middle_ini}\middle\conf\middle.ini"

    elif sys == "Linux":
        js_path = f"{hdoc_path}/js/Common.js"
        middle_ini = abspath.split("/webexpress")[0]
        middle_ini = f"{middle_ini}/middle/Conf/middle.ini"


    # hdoc_path = r"D:\demo\hdoc"
    # middle_ini = r"D:\demo\middle.ini"

    # html文件集合
    #lst_files = list(all_files(hdoc_path, '*.html;*.css;*.js;*.json'))

    lst_files = list(all_files(hdoc_path, '*.html;*.css;*.js;'))
    print(lst_files)
    conding_format = check_codeing_format(middle_ini)
    oper(db_host, lst_files, hdoc_path, middle_ini)
    lst_files = list(all_files(hdoc_path, '*.html;*.css;*.js;'))
