'''
文件比较，生成替换脚本
输入目录是完整路径
'''
# version 1.3 修改cp \r问题
import os, sys, stat
from pathlib import Path


def look_in_directory(file_to_find, directory):
    for f in os.listdir(directory):

        if f == file_to_find:
            # writeStr = "cp -f " + "./" + f + " /" + os.path.abspath(os.path.join(directory, f))
            writeStr = "cp -f " + "./" + f +  " " + os.path.abspath(os.path.join(directory, f))
            writeStr = writeStr.replace("\\", "/")
            if writeStr[writeStr.rfind("/")+1:].find(".") != -1:
                # writeStr = "/" + writeStr[0:writeStr.rfind("/")]
                writeStr =  writeStr[0:writeStr.rfind("/")]
            else:
                writeStr =  writeStr

            file.write(writeStr)
            file.write("\n")
            print("Found file: " + os.path.join(directory, f))
            # return True
        if os.path.isdir(os.path.join(directory, f)):
            if look_in_directory(file_to_find, os.path.join(directory, f)):
                return True

catalog = input("请输入您的目录名称：")
# rootpath = Path(os.path.abspath('./' + catalog))  # 获取要读取的路径
rootpath =Path(os.path.abspath( catalog))  # 获取要读取的路径
if rootpath.is_dir() == False:
    print("目录不存在")
    exit()

catalogSea = input("请输入您要查询的目录名称：")
# seaPath = Path(os.path.abspath('./' + catalogSea))  # 获取要查询的路径
seaPath = Path(os.path.abspath( catalogSea))  # 获取要查询的路径
if seaPath.is_dir() == False:
    print("目录不存在")
    exit()

sCreateFile = str(rootpath) + "/run.sh"
file = open(sCreateFile, 'w')
os.chmod(sCreateFile, stat.S_IRWXU)
file.write("#!/bin/bash")
file.write("\n")


rootDir = os.listdir(rootpath)
for val in rootDir:
    print(val)
    look_in_directory(val, seaPath)


