#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/27 0027 16:48
# @Author  : Zhang YP
# @Email   : 1579922399@qq.com
# @github  :  Aaron Ramsey
# @File    : request_test.py

import urllib, json, requests

from datetime import datetime

# def get_token():
#     tokenParams ={'iss':'adtoken','secret':'cdta91ldDaqlcdqj'}
#     token = requests.get("http://127.0.0.1:8000/getToken",params=tokenParams)
#     return json.loads(token.content)['token']

# 测试
url = "http://127.0.0.1:8000/walmart_account"
params = {'skip': 0, 'limit': 12}
request = requests.get(url=url, params=params)
response = request.content
print(json.loads(response.decode()))

# 下载文件
# startTime = datetime.now()
# url = "http://127.0.0.1:8000/download_station_folder"
# token = "468a998a670b1ed7695cd0f5ac3850db"
# params = {'token':token}
# data = {'station':'kimiss'}
# request = requests.post(url=url, params=params,json=data)
# response = request.content
# files_save_dirname = r"C:\Users\Administrator\Desktop\zouminy_de123.zip"
# with open(files_save_dirname, 'wb') as f:
#     f.write(response)
# print(f'下载花费:{(datetime.now()-startTime).total_seconds()}秒.')


# # # 上传文件
# startTime = datetime.now()
# url = "http://127.0.0.1:8000/upload_station_folder"
# token = "468a998a670b1ed7695cd0f5ac3850db"
# params = {'token': token}
# uploadFilePath = r"C:\Users\Administrator\Desktop\zouminy_de.zip"
# file = {"upload_file": open(uploadFilePath, 'rb')}
# data = {'station': 'kimiss'}
# request = requests.post(url=url, params=params,files=file)
# response = request.content
# print(response)
# # print(f'下载花费:{(datetime.now()-startTime).total_seconds()}秒.')
