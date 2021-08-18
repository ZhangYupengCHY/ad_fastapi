#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/8 0008 9:52
# @Author  : Zhang YP
# @Email   : 1579922399@qq.com
# @github  :  Aaron Ramsey
# @File    : crud.py


from sqlalchemy.orm import Session,load_only
import json

from sql_app import models, schema,query_table
from public_function import public_function,query_frequently_table_info


def get_walmart_account(db: Session, user_id: int = None, user_account: str = None):
    """
    查询walmart账号信息
    :param db:
    :type db:
    :param user_id:
    :type user_id:
    :param user_account:
    :type user_account:
    :return:
    :rtype:
    """
    if (user_id is None) and (user_account is None):
        raise TypeError('user_id 和 user_account 不能同时为空')
    if user_id is not None:
        if not public_function.is_variables_types_valid({user_id: int}):
            raise TypeError(f'user_id输入的数据类型不对.')
        return db.query(models.WalmartAccount).filter(models.WalmartAccount.id == user_id).first()
    if user_account is not None:
        if not public_function.is_variables_types_valid({user_account: str}):
            raise TypeError(f'user_account输入的数据类型不对.')
        return db.query(models.WalmartAccount).filter(models.WalmartAccount.account == user_account).first()


def get_all_walmart_accounts(db: Session, skip: int = 0, limit: int = None):
    """
    获取walmart全部账号信息
    :param db:
    :type db:
    :return:
    :rtype:
    """
    if not public_function.is_variables_types_valid({skip: int}):
        raise TypeError('skip 输入类型是整数')
    if limit is not None:
        if not public_function.is_variables_types_valid({limit: int}):
            raise TypeError('limit 输入类型是整数')
    return db.query(models.WalmartAccount).offset(skip).limit(limit).all()


def delete_walmart_account(db: Session, user_id: int = None, user_account: str = None):
    """
    删除wlamart账号
    :param db:
    :type db:
    :param user_id:
    :type user_id:
    :param user_account:
    :type user_account:
    :return:
    :rtype:
    """
    if (user_id is None) and (user_account is None):
        raise TypeError('user_id 和 user_account 不能同时为空')
    if user_id is not None:
        if not public_function.is_variables_types_valid({user_id: int}):
            raise TypeError(f'user_id输入的数据类型不对.')
        delete_walmart_account = db.query(models.WalmartAccount).filter(models.WalmartAccount.id == user_id).first()
    if user_account is not None:
        if not public_function.is_variables_types_valid({user_account: str}):
            raise TypeError(f'user_account输入的数据类型不对.')
        delete_walmart_account = db.query(models.WalmartAccount).filter(
            models.WalmartAccount.account == user_account).first()
    if delete_walmart_account:
        db.delete(delete_walmart_account)
        db.commit()
        db.flush()
        return delete_walmart_account


def update_walmart_account(db: Session, user_id: int = None, user_account: str = None):
    if (user_id is None) or (user_account is None):
        raise TypeError('user_id 和 user_account 不能为空')
    oldAccountInfo = db.query(models.WalmartAccount.account == user_account).first()
    if oldAccountInfo:
        db.commit()
        db.flush()
        db.refresh(db_item)
        return db_item



def query_high_quality_words(db:Session,station:str = None,erpsku:str = None,asin:str=None,sku:str=None,stationLimitNumber=4,queryLimit=1000,skip=0,pageLimit=1000,chooseColumns=None):
    """共享关键词查询"""
    if (not isinstance(skip,int)) or (not isinstance(pageLimit,int)):
        return '查询参数类型错误'
    if pageLimit not in range(1000,3001):
        return '单次查询个数范围不符合条件.'
    offset = skip * pageLimit

    if not any([station,erpsku,asin,sku]):
        return 'station,erpsku,asin,sku不能同时为空'
    if len([value for value in [station,erpsku,asin,sku] if value is not None]) != 1:
        return 'station,erpsku,asin,sku同时只能查询一个'

    if station is not None:
        if ',' not in station:
            return db.query(models.HighQualityKeyword).filter(models.HighQualityKeyword.station == station).all()
        else:
            queryStations = public_function.database_query_str_2_list(station)
            if len(queryStations) > stationLimitNumber:
                return '站点查询长度不得超过4'
            queryStations  =[public_function.standardStation(station) for station in queryStations if len(station) >1]
            return db.query(models.HighQualityKeyword).filter(models.HighQualityKeyword.station.in_(queryStations)).all()
    elif erpsku is not None:
        if ',' not in erpsku:
            if chooseColumns is None:
                return db.query(models.HighQualityKeyword).filter(models.HighQualityKeyword.erpsku == erpsku).offset(offset).limit(pageLimit).all()
            else:
                return db.query(models.HighQualityKeyword).options(load_only(*chooseColumns)).filter(models.HighQualityKeyword.erpsku == erpsku).offset(
                    offset).limit(pageLimit).all()
        else:
            queryErpSkuLen = public_function.database_query_str_2_list(erpsku)
            if len(queryErpSkuLen) > queryLimit:
                return f'单次erpsku查询个数不得超过{queryLimit}'
            if chooseColumns is None:
                return db.query(models.HighQualityKeyword).filter(models.HighQualityKeyword.erpsku.in_(queryErpSkuLen)).offset(offset).limit(pageLimit).all()
            else:
                return db.query(models.HighQualityKeyword).options(load_only(*chooseColumns)).filter(
                    models.HighQualityKeyword.erpsku.in_(queryErpSkuLen)).offset(offset).limit(pageLimit).all()
    elif asin is not None:
        if ',' not in asin:
            return db.query(models.HighQualityKeyword).filter(models.HighQualityKeyword.asin == asin).all()
        else:
            queryAsinLen = public_function.database_query_str_2_list(asin)
            if len(queryAsinLen) > queryLimit:
                return f'单次asin查询个数不得超过{queryLimit}'
            return db.query(models.HighQualityKeyword).filter(models.HighQualityKeyword.asin.in_(queryAsinLen)).all()
    else:
        if ',' not in sku:
            return db.query(models.HighQualityKeyword).filter(models.HighQualityKeyword.sku == sku).all()
        else:
            querySkuLen = public_function.database_query_str_2_list(sku)
            if len(querySkuLen) > queryLimit:
                return f'单次sku查询个数不得超过{queryLimit}'
            return db.query(models.HighQualityKeyword).filter(models.HighQualityKeyword.sku.in_(querySkuLen)).all()



def query_cx_sku_match(db:Session,erp_sku:str = None,seller_sku:str=None,queryLimit=1000):
    """共享楚晋sku捆绑表关键词查询"""
    if not any([erp_sku,seller_sku]):
        return 'erp_sku,seller_sku不能同时为空'
    if len([value for value in [erp_sku,seller_sku] if value is not None]) != 1:
        return 'erp_sku,seller_sku同时只能查询一个'
    exportColumns = ['seller_sku','sku']
    if erp_sku is not None:
        if ',' not in erp_sku:
            return db.query(models.YibaiAmazonSkuMap).options(load_only(*exportColumns)).filter(models.YibaiAmazonSkuMap.sku == erp_sku).all()
        else:
            queryErpSkuLen = public_function.database_query_str_2_list(erp_sku)
            if len(queryErpSkuLen) > queryLimit:
                return f'单次erp_sku查询个数不得超过{queryLimit}'
            return db.query(models.YibaiAmazonSkuMap).options(load_only(*exportColumns)).filter(models.YibaiAmazonSkuMap.sku.in_(queryErpSkuLen)).all()
    else:
        if ',' not in seller_sku:
            return db.query(models.YibaiAmazonSkuMap).options(load_only(*exportColumns)).filter(models.YibaiAmazonSkuMap.seller_sku == seller_sku).all()
        else:
            querySkuLen = public_function.database_query_str_2_list(seller_sku)
            if len(querySkuLen) > queryLimit:
                return f'单次seller_sku查询个数不得超过{queryLimit}'
            return db.query(models.YibaiAmazonSkuMap).options(load_only(*exportColumns)).filter(models.YibaiAmazonSkuMap.seller_sku.in_(querySkuLen)).all()


def query_clear_sku(db:Session,account_id:str,limit=100000):
    if not isinstance(account_id,(str,int)):
        return f'查询的类型不对,{type(account_id)}不是有效的数据类型.'
    return db.query(models.ClearSku).filter(models.ClearSku.account_id == account_id).limit(limit).all()


def query_account_id_by_name(db:Session,account_name):
    if not isinstance(account_name,(str,list,set)):
        return None
    if isinstance(account_name,str):
        account_name = public_function.standardStation(account_name)
        queryAccountIdInfo = db.query(models.AccountIdIndex).options(load_only('id')).filter(models.AccountIdIndex.account_name == account_name).values('id')
        queryAccountIdInfo = list(queryAccountIdInfo)
        if len(queryAccountIdInfo) > 0:
            return queryAccountIdInfo[0][0]
        else:
            return None
    else:
        account_name = [public_function.standardStation(account) for account in account_name]
        exportColumns = ['id',"account_name"]
        queryAccountIdInfo = db.query(models.AccountIdIndex).options(load_only(*exportColumns)).filter(
            models.AccountIdIndex.account_name.in_(account_name)).all()
        if len(queryAccountIdInfo)>0:
            account_name_id_dict = {one_row.account_name:one_row.id for one_row in queryAccountIdInfo}
            return {account_:account_name_id_dict.get(account_,None) for account_ in account_name}
        else:
            return {account_:None for account_ in account_name}

#
# def sku_inventory(db: Session, accounID, sku):
#     """
#
#     逻辑：
#     afn_reserved_quantity = 0 或者  reserved_fc-transfers + reserved_fc-processing = 0的时候，转运库存 = 0
#     否则  转运库存 = reserved_fc-transfers + reserved_fc-processing
#     总可用库存 = afn_fulfillable_quantity + 转运库存 + afn_researching_quantity
#
#     其中yibai_amazon_fba_inventory_month_end表中要做筛选month = 当天,condition = New
#
#     """
#     if not isinstance(accounID, int):
#         return
#     if not isinstance(sku, (set, list)):
#         return
#     if len(sku) == 0:
#         return
#     # 获取当前的库存信息
#     exportColumns = ['reserved_fc_transfers', 'reserved_fc_processing']
#     rightNowQTY = db.query(models.YibaiAmazonReservedInventory).options(load_only(*exportColumns)).filter(
#         (models.YibaiAmazonReservedInventory.account_id == accounID) & (
#             models.YibaiAmazonReservedInventory.sku.in_(sku))).all()
#     # 获取历史中的库存信息
#     nowDate = datetime.now().date()
#     monthlExportColumns = ['afn_reserved_quantity', 'afn_fulfillable_quantity','afn_researching_quantity']
#     monthlyQTY = db.query(models.YibaiAmazonFbaInventoryMonthEnd).options(load_only(*monthlExportColumns)).filter(
#         (models.YibaiAmazonFbaInventoryMonthEnd.month == nowDate) & (models.YibaiAmazonFbaInventoryMonthEnd.condition == 'New') &
#         (models.YibaiAmazonFbaInventoryMonthEnd.account_id == accounID) &(models.YibaiAmazonFbaInventoryMonthEnd.sku.in_(sku))).all()
#     return rightNowQTY,monthlyQTY
