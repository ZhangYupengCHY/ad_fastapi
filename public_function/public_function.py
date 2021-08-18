#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/8 0008 10:18
# @Author  : Zhang YP
# @Email   : 1579922399@qq.com
# @github  :  Aaron Ramsey
# @File    : public_function.py

import pandas as pd


def series_to_int(series):
    """
    将series转换为数值型
    Parameters
    ----------
    series :
    fillna :

    Returns
    -------

    """
    return [int(value) if pd.notna(value) else 0 for value in series]


def wrong_type_raise_msg(func_name, variable_name, input_type, default_type):
    """
    当函数的参数的输入类型发生错误时,给的错误提示
    Parameters
    ----------
    func_name :str
        函数名
    variable_name :str
        参数类型输入错误的参数名
    input_type :str
        输入的错误的参数类型
    default_type :str
        需要输入的参数类型

    Returns
    -------
        str:
            错误提示
    """
    return f"函数:{func_name}的参数:{variable_name}的输入类型应该是:{default_type},而输入的类型是:{input_type}."


def is_variables_types_valid(variables_types: dict):
    """
    验证函数中输入参数的类型是否正确
    Parameters
    ----------
    variables_types : dict of list or set
        需要验证的参数名
    Returns
    -------
        bool:True,False,None
    """
    func_name = is_variables_types_valid.__name__
    # 输入类型验证
    if not isinstance(variables_types, dict):
        raise TypeError(f'{func_name}:判断数据类型应该数据字典')
    for variable, variableType in variables_types.items():
        if not isinstance(variableType, (type, tuple)):
            raise TypeError(f'{func_name}:{variable}的值应该输入数据类型.')
        if not isinstance(variable, variableType):
            return False
    return True


def standardStation(stationName, case='lower'):
    """规范站点的命名"""
    if (stationName is None) or (not isinstance(stationName, str) or (len(stationName.strip()) == 0)):
        return ''
    if case not in ['lower', 'upper']:
        raise ValueError('case must lower or upper')
    if case == 'lower':
        return stationName.strip().replace('-', '_').replace(' ', '_').lower()
    else:
        return stationName.strip().replace('-', '_').replace(' ', '_').upper()


def database_query_str_2_list(queryStr,splitSign=','):
    if not isinstance(queryStr,str):
        return []
    if splitSign not in queryStr:
        return []
    else:
        splitSign = splitSign.strip()
        queryList = queryStr.split(splitSign)
        queryList = [query for query in queryList if query != '']
        return queryList

