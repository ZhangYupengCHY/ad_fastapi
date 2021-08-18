#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/7 0007 10:01
# @Author  : Zhang YP
# @Email   : 1579922399@qq.com
# @github  :  Aaron Ramsey
# @File    : process_file.py

"""
处理文件相关的
"""


import os,time
import pandas as pd
from datetime import datetime


def read_excel(path):
    if not os.path.exists(path):
        return
    if os.path.splitext(path)[1].lower() not in ['.xls','.xlsx']:
        return 'file type is not Excel:{path} .'
    REPORT_ENCODINGS = ('utf-8', 'utf-16', "latin_1", "ISO-8859-1", 'cp932', 'unicode_escape','gbk')
    for encodingType in REPORT_ENCODINGS:
        try:
            return pd.read_excel(path, encoding=encodingType)
        except:
            continue
    return f"cant read excel file:{path} ."


def is_file(filePath):
    # 是否是有效的文件路径
    return os.path.exists(filePath)


def is_folder(path):
    """判断是不是有效的文件夹"""
    return os.path.isdir(path)

# 1 '''把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12'''
def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


def str2datetime(str,format='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(str,format)

# 2、'''获取文件的大小,结果保留两位小数，单位为MB'''
def file_size(filePath):
    # filePath = unicode(filePath,'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)


# 3、　　'''获取文件的访问时间'''
def file_access_time(filePath):
    # filePath = unicode(filePath,'utf8')
    t = os.path.getatime(filePath)
    return TimeStampToTime(t)


# 4、　　'''获取文件的创建时间'''
def file_create_time(filePath):
    # filePath = unicode(filePath,'utf8')
    t = os.path.getctime(filePath)
    return TimeStampToTime(t)


# 5、　　'''获取文件的修改时间'''
def file_modify_time(filePath):
    # filePath = unicode(filePath,'utf8')
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)


def read_file_as_bytes(filePath):
    if not os.path.exists(filePath):
        return
    else:
        with open(filePath,'rb') as f:
            data = f.read()
        return data

