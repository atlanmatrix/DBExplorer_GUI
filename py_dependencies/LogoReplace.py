# logo替换
import os
import shutil

print('类别转换过程中必须先转成监控易之后再转换成其它，比如：现在是IT如果要装成山西电力，必须先转成监控易之后再转成山西电力。类别关系如下：\n 1——IT\n 2——监控易\n 3——山西电力\n 4——浪思\n 5——云监控')
types = {1: 'IT', 2: 'jky', 3: 'sx',4:'Langsi',5:'cloud'}
input_ = int(input('请输入替换的类别：'))
tmp = ['images/fequency/kslogo.png', 'images/fequency/jkyLogo.png', 'css/img/logo_lg.svg', 'images/bigCommon/logo.png',
       'images/overview_fonfig/jkyLogo.png', 'css/img/logo_lg.png', 'js/Common.js', 'login.html']

rootPath = os.path.abspath('..')+'/hdoc/'

logofile_path = rootPath + 'login_files'

web_path = rootPath + 'LogoFile/'+ types[input_]
try:
#批量替换图片和html
    for val in tmp:
        if val == 'login.html':
            replacePath = web_path +'/'+ val
        else:
            num = val.rfind('/')
            replacePath = web_path + val[num:]
        shutil.copy(replacePath, rootPath + val)

    os.chdir(web_path + "/login_files")
    #替换login_files文件夹
    shutil.rmtree(logofile_path)
    shutil.copytree(web_path + "/login_files", logofile_path)


    #修改base_menu注释关于和帮助
    with open(rootPath+'/js/base_menu.js','r',encoding='UTF-8') as f_obj:
        data = f_obj.readlines()
        for key,val in enumerate(data):
            if val.find('OEMBEGIN') != -1:
                if types[input_] == 'jky':
                    data[key+1] = data[key+1][2:]
                else:
                    data[key+1] = '/*' +data[key+1]
            if  val.find('OEMEND') != -1:
                if types[input_] == 'jky':
                    data[key] = data[key][2:]
                else:
                    data[key-1] = data[key-1] + '*/'

        string = ''.join(data)
        f_obj.close()

    with open(rootPath+'/js/base_menu.js','w',encoding='UTF-8') as f:
        f.write(string)
        f.close()
except Exception as e:
    print(e)
    exit()
print('替换成功')