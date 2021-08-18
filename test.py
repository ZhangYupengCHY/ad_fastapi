#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/27 0027 18:38
# @Author  : Zhang YP
# @Email   : 1579922399@qq.com
# @github  :  Aaron Ramsey
# @File    : test.py

import pandas as pd
import io


import json, requests
from urllib import parse
"""
    查询站点sku库存表
"""

import json, requests,os

windowHost = "http://172.16.128.240:8000"


def query_dirlist(path):
    url = parse.urljoin(windowHost, 'dirlist/')
    # url = 'http://172.16.128.240:8000/dirlist/'
    # 参数名
    params = {'dir_path': path}
    request = requests.get(url=url, params=params, timeout=(3, 7))
    response = request.content
    return json.loads(response)


def is_path_exist(path):
    url = parse.urljoin(windowHost, 'file_exist/')
    params = {'file_path': path}
    request = requests.get(url=url, params=params, timeout=(3, 7))
    response = request.content
    return json.loads(response)


def download_file(path):
    url = parse.urljoin(windowHost, 'download_file/')
    params = {'file_path': path}
    request = requests.get(url=url, params=params, timeout=(3, 7))
    if request.status_code == 200:
        response = request.content
        try:
            return json.loads(response)['detail']
        except:
            return response
    else:
        return f'cant connect {path}'


class Trans_file(object):
    """处理广告后台中(Linux)与文件服务器(Windonw)中文件传输"""

    window_server_folder ={'seller_five':'F:/sales_upload_zipped'}

    @staticmethod
    def __upload__file__(savePath,fileBytes):
        post = requests.post(url=parse.urljoin(windowHost, 'upload_file/'), params={'savePath': savePath},
                             files={"fileBytes": fileBytes}, timeout=(3, 20))
        if post.status_code == 200:
            return 'success'
        else:
            return 'fail'


    @staticmethod
    def upload_five_zip(saveName,fileBytes):
        """上传销售回传的五表文件"""
        savePath = os.path.join(Trans_file.window_server_folder['seller_five'],saveName)
        message = Trans_file.__upload__file__(savePath,fileBytes)
        return message

    @staticmethod
    def download_file(path):
        """下载文件"""
        url = parse.urljoin(windowHost, 'download_file/')
        params = {'file_path': path}
        request = requests.get(url=url, params=params, timeout=(3, 7))
        if request.status_code == 200:
            response = request.content
            try:
                return json.loads(response)['detail']
            except:
                return response
        else:
            return f'cant connect {path}'

    @staticmethod
    def download_file_bytes(path):
        """下载文件"""
        url = parse.urljoin(windowHost, 'fileBytes/')
        params = {'file_path': path}
        request = requests.get(url=url, params=params, timeout=(3, 7))
        if request.status_code == 200:
            response = request.content
            try:
                return json.loads(response)['detail']
            except:
                return response
        else:
            return f'cant connect {path}'

    @staticmethod
    def delete_file(path):
        """删除文件"""


if __name__ == '__main__':
    sku = 'TJA02678,QC17419'
    url = 'http://172.16.128.240:8000/query_kws_by_erpsku/'
    token = '468a998a670b1ed7695cd0f5ac3850db'
    params = {'token':token,'erpsku':sku,'page':1,'size':1000}
    request = requests.get(url=url, params=params, timeout=(3, 7))
    response = request.content
    print(1)






