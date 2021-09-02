#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/7 0007 16:41
# @Author  : Zhang YP
# @Email   : 1579922399@qq.com
# @github  :  Aaron Ramsey
# @File    : database.py


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sql_app.models import Base,Base_kws

# 默认的

CONN_DB = {
    'team_station':{'ip':'172.16.128.240','port':3306,'user':'marmot','password':'marmot123','db':'team_station'},
    'kws':{'ip':'172.16.128.240','port':3306,'user':'marmot','password':'marmot123','db':'server_camp_report'},
    # 楚讯站点的sku捆绑表
    'cx_sku_match':{'ip':'124.71.59.209','port':3306,'user':'zhangyupeng','password':'zypYB&^^234','db':'yibai_product_cx'},
    # 站点sku的库存
    'sku_inventory':{'ip':'139.9.206.7','port':3306,'user':'wangyan','password':'wyYB&^%523435','db':'yibai_product'},
}


class db_connect:

    @staticmethod
    def create_engine(server=CONN_DB['team_station']['ip'],user=CONN_DB['team_station']['user'],password=CONN_DB['team_station']['password'],port=CONN_DB['team_station']['port'],db=CONN_DB['team_station']['db'],charset='utf8'):
        url: str = f'mysql+pymysql://{user}:{password}@{server}:{port}/{db}?charset={charset}'
        return create_engine(url, pool_pre_ping=True)


# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind={Base:db_connect.create_engine(db=MYSQL_DB),Base_kws:db_connect.create_engine(db=MYSQL_KWS_DB)})
SessionTeamStation = sessionmaker(autocommit=False, autoflush=False, bind=db_connect.create_engine(db=CONN_DB['team_station']['db']))
SessionKws = sessionmaker(autocommit=False, autoflush=False, bind=db_connect.create_engine(db=CONN_DB['kws']['db']))
SessionCXSKUMATCH = sessionmaker(autocommit=False, autoflush=False, bind=db_connect.create_engine(server=CONN_DB['cx_sku_match']['ip'],user=CONN_DB['cx_sku_match']['user'],password=CONN_DB['cx_sku_match']['password'],port=CONN_DB['cx_sku_match']['port'],db=CONN_DB['cx_sku_match']['db']))
SessionSKUINVENTORY = sessionmaker(autocommit=False, autoflush=False, bind=db_connect.create_engine(server=CONN_DB['sku_inventory']['ip'],user=CONN_DB['sku_inventory']['user'],password=CONN_DB['sku_inventory']['password'],port=CONN_DB['sku_inventory']['port'],db=CONN_DB['sku_inventory']['db']))

