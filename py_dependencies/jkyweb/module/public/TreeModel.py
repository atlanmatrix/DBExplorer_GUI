# -*- coding: UTF-8 -*-
# @Author: yh
# @Time: 2020/11/5 16:18
# @Remark: 存放Tree db数据库的操作方法，详情见TreeModel使用手册

from superbsapi import *

from BSDb.VariableData import *
from BSDb.bserror import BS_NOERROR
from BSDb.treedb_def import *
from pyconfig.dbconfig import dbconfig

symbol_map = {
    'e': TRDB_FMC_EQUAL,  # 等于
    'ne': TRDB_FMC_UNEQUAL,  # 不等于
    'gt': TRDB_FMC_GREATERTHAN,  # 大于
    'lt': TRDB_FMC_LESSTHAN,  # 小于
    'gte': TRDB_FMC_EQUALORGREATERTHAN,  # 大于等于
    'lte': TRDB_FMC_EQUALORLESSTHAN,  # 小于等于

    'like': TRDB_FMC_LIKE,  # 模糊匹配，使用 * 做为通配符
    'nclike': TRDB_FMC_NOCASE_LIKE,  # 模糊匹配，不区分大小写
    'in': TRDB_FMC_RANGE,  # 范围查找
    'between': TRDB_FMC_RANGE  # 范围查找（范围）
    # 其他的类型，以后用到了再添加
}
type_map = {
    'str': VDT_STR,
    'float': VDT_FLOAT,
    'double': VDT_DOUBLE,
    'int': VDT_I32,
    'int8': VDT_I8,
    'int64': VDT_I64,

    'ui8': VDT_UI8,
    'ui64': VDT_UI64,
    'time': VDT_TIME,
    'timestr': VDT_TIMESTR,
    'empty': VDT_EMPTY
    # 其他的类型，以后用到了再添加
}


class TreeModel(object):

    def __init__(self):
        self.__chl = CBSHandleLoc()

    @staticmethod
    def return_value(res):
        """
        用于直接返回结果集的函数，处理其返回值
        :param res: 错误信息及函数返回的数据 (str/tuple)
        :return: 返回信息
        """
        msg = res[0] if isinstance(res, tuple) else res
        assert msg == BS_NOERROR, msg
        if res:
            return res[1] if len(res) == 2 else res[1:]
        return None

    def exec_tree(self, operate, *args, **kwargs):
        """
        用于执行Tree db开头的函数
        :param operate: 使用的函数
        :param args kwargs: 函数所使用的变量
        :return: 执行结果
        """
        func = getattr(self.__chl, operate)
        res = func(*args, **kwargs)
        return self.return_value(res)

    def exec_bs(self, operate, *args, **kwargs):
        """
        用于执行bs开头的函数
        :param operate: 使用的函数
        :param args kwargs: 函数所使用的变量
        :return: 执行结果
        """
        res = eval(operate)(self.__chl.GetConfHandle(), *args, **kwargs)
        return self.return_value(res)

    def begin(self):
        """
        开启事务
        """
        self.exec_tree('Treedb_BeginTransaction')

    def commit(self):
        """
        提交事务
        :return:
        """
        self.exec_tree('Treedb_CommitTransaction')

    def rollback(self):
        """
        回滚事务
        """
        self.exec_tree('Treedb_RollbackTransaction')

    def open(self, main_key, sub_key=None, host='127.0.0.1', file='master', main_key_pwd='', flag=None,
             port=dbconfig.ndbport, path_flag=False):
        """
        打开数据库键 [只打开主键或子键 / 同时打开主键和子键（子键路径）]
        :param main_key: 主键名
        :param sub_key: 子键名
        :param host: 主机名
        :param file: 数据库名
        :param main_key_pwd: 主键密码
        :param flag: 打开风格
        :param port: 端口号
        :param path_flag: 如果路径上有子键不存在是否自动创建
        :return: 类对象
        """
        if not flag:
            if sub_key:
                flag = TRDB_OPKF_OPENEXIST if '\\' in sub_key else TRDB_OPKF_DOTPATH
            else:
                flag = TRDB_OPKF_OPENEXIST if '\\' in main_key else TRDB_OPKF_DOTPATH

        if sub_key:
            try:
                self.exec_tree('Treedb_ReopenMainKey', sub_key, flag, path_flag, main_key, main_key_pwd, file)
            except AssertionError:
                try:
                    print('222222222222222222222打开-mk-' + main_key + '-sk-' + sub_key)
                    self.__chl = CBSHandleLoc()
                    self.exec_tree('Treedb_Alloc', host, file, main_key, main_key_pwd, TRDB_OPKF_OPENEXIST, port)
                    self.exec_tree('Treedb_ReopenSubKey', sub_key, flag)
                except Exception:
                    raise AssertionError('打开数据库键失败-mk-' + main_key + '-sk-' + sub_key)
        else:
            try:
                self.exec_tree('Treedb_ReopenSubKey', main_key, flag)
            except Exception:
                try:
                    self.exec_tree('Treedb_ReopenMainKey', '', flag, path_flag, main_key, main_key_pwd, file)
                except Exception:
                    try:
                        print('1111111111111111111111111111111111111打开-' + main_key)
                        self.__chl = CBSHandleLoc()
                        self.exec_tree('Treedb_Alloc', host, file, main_key, main_key_pwd, TRDB_OPKF_OPENEXIST, port)
                    except Exception:
                        raise AssertionError('打开数据库键失败-' + main_key)
        return self

    def sub_keys(self) -> list:
        """
        获取当前键下所有的子键名
        :return: 子键列表
        """
        res_list = list()
        self.exec_tree('Treedb_GetAllSubKeys', res_list)
        return res_list

    def sub_items(self, key_list=None, prop_list=None) -> dict:
        """
        获取当前键下，指定子键，指定属性的 key-value键值对
        :param key_list: 要获取的子键列表
        :param prop_list: 要获取的属性列表
        :return: 子键及其属性字典
        """
        res_dict = dict()
        if isinstance(key_list, str):
            key_list = [key_list]
        if isinstance(prop_list, str):
            prop_list = [prop_list]

        self.exec_bs('bs_treedb_get_subkey_properties', key_list if key_list else [],
                     prop_list if prop_list else [], res_dict)
        return res_dict

    def items(self, prop_list=None) -> dict:
        """
        获取当前键下、指定属性的 key-value键值对
        :param prop_list: 要获取属性
        """
        prop_list = [prop_list] if isinstance(prop_list, str) else prop_list

        res_dict = dict()
        self.exec_bs('bs_treedb_get_properties', prop_list if prop_list else [], res_dict)
        return res_dict

    def props(self) -> list:
        """
        获取所有属性名
        :return: 属性名列表
        """
        res_list = list()
        self.exec_tree('Treedb_GetAllPropertyNames', res_list)
        return res_list

    def fetchone_value(self, prop_name: str):
        """
        获取一个属性的值
        :param prop_name: 要获取的属性名称
        :return: 属性值
        """
        return self.exec_tree('Treedb_GetProperty', prop_name)

    def create_main_key(self, main_key, host=dbconfig.szdbserver, file='base', main_key_pwd='',
                        port=dbconfig.ndbport):
        # TODO 以后要用到了再写吧
        # self.exec_tree('Treedb_CreateMainKey', host, file, main_key, main_key_pwd, port)
        pass

    def insert_sub_key(self, sub_key='', flag=TDDB_OPKF_CREATEDYNKEY) -> str:
        """
        插入一个子键
        :param sub_key: 子键名（不传会自动生成子键名并返回）
        :param flag: 打开风格
        :return: 插入的子键名 str
        """
        return self.exec_tree('Treedb_InsertSubKey', sub_key, flag)

    def insert_sub_keys(self, sub_keys, flag=TDDB_OPKF_CREATEDYNKEY):
        """
        批量插入子键
        :param sub_keys: 子键列表
        :param flag: 打开风格
        """
        for sub_key in sub_keys:
            self.exec_tree('Treedb_InsertSubKey', sub_key, flag)

    def insert_item(self, prop, value, overwrite=True):
        """
        插入一条数据
        :param prop: 键
        :param value: 值
        :param overwrite: 是否覆盖原值
        """
        value_type = type_map.get(type(value).__name__)
        assert value_type, '请输入正确的查询参数！name及vLiData，详情见TreeModel使用手册'
        self.exec_bs('bs_treedb_insert_property', prop, value, value_type, overwrite)

    def insert_items(self, items, overwrite=True):
        """
        批量插入数据
        :param items: 插入的数据，格式：[(k1, v1), (k2, v2)]
        :param overwrite: 是否覆盖原值
        """
        assert isinstance(items, list), '错误的数据类型，items应为列表'
        for item in items:
            assert isinstance(item, tuple) and len(item) in [2, 3], '错误的数据类型，items列表中的数据应为元组且长度为2或3'
            assert type_map.get(item[2]) if len(item) == 3 else type_map.get(
                type(item[1]).__name__), '无法获取到value的类型！如果您未手动传入类型或确信传入类型正确，请于文件首部type_map中添加此类型'
            value_type = type_map[item[2]] if len(item) == 3 else type_map[type(item[1]).__name__]
            self.exec_bs('bs_treedb_insert_property', item[0], item[1], value_type, overwrite)

    def insert_key_items(self, items, key=None, overwrite=True):
        """
        批量插入子键及k,v
        :param items: 插入的数据，格式：[(k1, v1), (k2, v2)]
        :param key: 子键名称,不传自动生成
        :param overwrite: 是否覆盖原值
        """
        assert isinstance(items, list), '错误的数据类型，items应为列表'
        items_dict = list()
        for item in items:
            assert isinstance(item, tuple) and len(item) in [2, 3], '错误的数据类型，items列表中的数据应为元组且长度为2或3'
            assert type_map.get(item[2]) if len(item) == 3 else type_map.get(
                type(item[1]).__name__), '无法获取到value的类型！如果您未手动传入类型或确信传入类型正确，请于文件首部type_map中添加此类型'
            value_type = type_map[item[2]] if len(item) == 3 else type_map[type(item[1]).__name__]
            items_dict.append({'name': item[0], 'value': item[1], 'valuetype': value_type})
        return self.exec_bs('bs_treedb_insert_key_and_properties', key if key else '', TRDB_OPKF_OPENEXIST, items_dict,
                            overwrite)

    def delete(self, keys=None):
        """
        删除 单个子键/子键列表/自身
        :param keys: 要删除的键，不传会删除自身
        """
        if isinstance(keys, list):
            for key in keys:
                self.exec_tree('Treedb_DeleteSubKey', key)
        elif isinstance(keys, str):
            self.exec_tree('Treedb_DeleteSubKey', keys)

        if keys is None:
            self.exec_bs('bs_treedb_delete_key')

    def delete_prop(self, prop: str):
        """
        删除一个属性、所有属性
        :param prop: 要删除的属性名
        """
        if prop:
            self.exec_tree('Treedb_DeleteProperty', prop)
        else:
            self.exec_tree('Treedb_DeleteAllProperty')

    def rename(self, old_key, new_key=None):
        """
        重命名一个子键、自身
        :param old_key: 要重命名的子键
        :param new_key: 新的名字
        （重命名自身的时候只需要传递新的名字）
        """
        if new_key:
            self.exec_tree('Treedb_RenameSubKey', old_key, new_key)
        else:
            self.exec_tree('Treedb_RenameThisKey', old_key)

    def rename_prop(self, old_prop: str, new_prop: str):
        """
        重命名一个属性
        :param old_prop: 要重命名的属性
        :param new_prop: 新的属性名
        """
        self.exec_tree('Treedb_RenameProperty', old_prop, new_prop)

    def filter(self, **kwargs):
        import re
        try:
            page_size = kwargs.pop('page_size')
            assert page_size, '未获取到数据！'
        except (KeyError, AssertionError):
            page_size = 0
        try:
            page_index = kwargs.pop('page_index')
            assert page_index, '未获取到数据！'
        except (KeyError, AssertionError):
            page_index = 1
        try:
            order_by = kwargs.pop('order_by')
            assert order_by, '未获取到数据！'
        except (KeyError, AssertionError):
            order_by = ''
        try:
            is_desc = kwargs.pop('is_desc')
        except KeyError:
            is_desc = False
        try:
            default_expression = kwargs.pop('default_expression')
            assert default_expression, '未获取到数据！'
        except (KeyError, AssertionError):
            default_expression = None
        args, range_conditions = list(), dict()

        expression = '0'
        in_flag = False

        for key, value in kwargs.items():
            res = re.match(r'([\S_]+)__(\S+)', key)
            if res is None:
                symbol = 'e'
            else:
                key, symbol = res.groups()
                assert symbol in symbol_map, '查询操作错误！正确操作包含：gt、lt等，详情见TreeModel使用手册'
            # if re.match(r'^[_]?[[0-9A-Za-z]+[_]?[0-9A-Za-z]+]*?$', key):
            #     symbol = 'e'
            # elif re.match(r'^[_]?[[0-9A-Za-z]+[_]?[0-9A-Za-z]+]*?__[0-9A-Za-z]+$', key):
            #     key, symbol = key.split('__')
            #     assert symbol in symbol_map, '查询操作错误！正确操作包含：gt、lt等，详情见TreeModel使用手册'
            # else:
            #     raise ValueError('查询格式错误！正确示例：name="test", vLiData__gt=3，详情见TreeModel使用手册')

            temp = {'key': key, 'value_type': type(value).__name__, 'symbol': symbol, 'value': value}

            if symbol == 'in':
                assert isinstance(value, list), '查询格式错误！正确示例：a__in=[1, 3, 4, 5]，详情见TreeModel使用手册'
                i = 0
                in_flag = True
                for v in value:
                    temp = {'key': key, 'value_type': type(v).__name__, 'symbol': 'e', 'value': v}
                    args.append(temp)
                    if i == 0:
                        expression = '(0'
                    else:
                        expression += ' or ' + str(i)
                    i += 1
                expression += ')'
                continue
            if symbol == 'between':
                assert isinstance(value, list) and len(value) in [2,
                                                                  3], '查询格式错误！正确示例：a__between=[1, 3]，详情见TreeModel使用手册'
                temp['range_conditions'] = {'vLiData': value[0], 'vEnd': value[1]}
                temp['value_type'] = value[2] if len(value) == 3 else type(value[0]).__name__
            args.append(temp)

        default_query_conditions = list()
        for arg in args:
            assert arg['symbol'] in symbol_map, '查询操作错误！正确操作包含：gt、lt等，详情见TreeModel使用手册'
            assert arg['value_type'] in type_map, '查询数据类型！正确操作包含：str、int等，详情见TreeModel使用手册'
            data = {'name': arg['key'], 'nCondition': symbol_map[arg['symbol']], 'vLiData': arg['value'],
                    'vLiDataType': type_map[arg['value_type']]}
            if arg.get('range_conditions'):
                data.update(arg['range_conditions'])
            default_query_conditions.append(data)

        if in_flag:
            for k in range(len(kwargs) - 1):
                expression += ' and ' + str(i + k)
        else:
            for k in range(len(kwargs) - 1):
                expression += ' and ' + str(k + 1)
        res_list = list()
        res = self.exec_bs('bs_treedb_query_subkey_by_condition_ex', default_query_conditions,
                           default_expression if default_expression else expression,
                           res_list, page_size, (page_index - 1) * page_size, order_by, is_desc)

        return res, res_list
