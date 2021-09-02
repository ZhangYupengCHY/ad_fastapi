#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/27 0027 17:44
# @Author  : Zhang YP
# @Email   : 1579922399@qq.com
# @github  :  Aaron Ramsey
# @File    : static.py

import base64
import hashlib



TOKEN = "468a998a670b1ed7695cd0f5ac3850db"

# 站点文件保存路径
STATIONFIVEFILESSAVEFOLDER = r"F:\station_folder"


# 远程五表请求文件保存路径
REMOTEFIVEFILESSAVEFOLDER = r"F:\five_reports_zipped"

# 上传表保存路径
UPLOADFILESAVEFOLDER = r"E:\AD_WEB\file_dir\station_upload_files"


# 国家与站点对应表
CN_EN_SITE_DICT = {'日本': 'JP', '印度': 'IN', '澳大利亚': 'AU', '美国': 'US', '加拿大': 'CA', '墨西哥': 'MX',
                      '英国': 'UK', '法国': 'FR', '德国': 'DE', '西班牙': 'ES', '意大利': 'IT', '中东': 'AE',
                   '中国': 'ZH', '荷兰': 'NL','巴西': 'BR','新加坡':'SG','瑞典':'SE','沙特':'SA','波兰':'PL','土耳其':'TR'}
