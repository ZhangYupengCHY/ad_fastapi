#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/27 0027 16:40
# @Author  : Zhang YP
# @Email   : 1579922399@qq.com
# @github  :  Aaron Ramsey
# @File    : schema.py

"""
定义请求参数
"""
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


class station(BaseModel):
    """
    站点名
    """
    station:str



class stationRequest(station):
    """
    请求站点报表
    """
    pass


