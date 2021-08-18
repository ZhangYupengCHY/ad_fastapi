#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/12 0012 19:52
# @Author  : Zhang YP
# @Email   : 1579922399@qq.com
# @github  :  Aaron Ramsey
# @File    : custom_logging.py

import os
import time
import logging
import sys
from pathlib import Path

import uvicorn
from loguru import logger
import json


basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"


# 定位到log日志文件
log_path = os.path.join(basedir, 'logs')

if not os.path.exists(log_path):
    os.mkdir(log_path)


log_path_all = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_log.log')
log_path_error = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_error.log')

logger.add(log_path_all, format="{time} {level} {message}", rotation="12:00", retention="5 days", enqueue=True,level="INFO")
logger.add(log_path_error, format="{time} {level} {message}", rotation="12:00", retention="5 days", enqueue=True,level="ERROR")

# 日志简单配置
# 具体其他配置 可自行参考 https://github.com/Delgan/loguru

# format 参数： {time} {level} {message}、  {time:YYYY-MM-DD at HH:mm:ss} | {level} | {message} 记录参数
# level 日志等级
# rotation 参数：1 week 一周、00:00每天固定时间、 500 MB 固定文件大小
# retention 参数： 10 days 日志最长保存时间
# compression 参数： zip 日志文件压缩格式
# enqueue 参数 True 日志文件异步写入
# serialize 参数： True 序列化json
# encoding 参数： utf-8 字符编码、部分情况会出现中文乱码问题
# logger.info('If you are using Python {}, prefer {feature} of course!', 3.6, feature='f-strings') 格式化输入内容
#  可通过等级不同对日志文件进行分割储存

