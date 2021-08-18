#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/27 0027 17:59
# @Author  : Zhang YP
# @Email   : 1579922399@qq.com
# @github  :  Aaron Ramsey
# @File    : accessManager.py


import hashlib

def hash_code(code,salt='ramsey'):
    #’默认的账号是adtoken 密码是cdta91ldDaqlcdqj‘
    if not isinstance(code,str):
        raise TypeError('code must string')
    saltedCode = code+salt
    saltedCode = saltedCode.encode(encoding='utf-8')
    m = hashlib.md5()
    m.update(saltedCode)
    return m.hexdigest()
