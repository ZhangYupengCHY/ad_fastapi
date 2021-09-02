#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/8 0008 11:02
# @Author  : Zhang YP
# @Email   : 1579922399@qq.com
# @github  :  Aaron Ramsey
# @File    : main.py
import json
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi import APIRouter,Depends,HTTPException,Body
from sqlalchemy.orm import Session
from loguru import logger

from public_function import query_frequently_table_info, public_function
from sql_app import models, schema, database, crud, query_table
import static
from sql_app.database import CONN_DB
from sql_app import models as app_models

# 使用fastapi-crudrouter快速构建curd
models.Base.metadata.create_all(bind=database.db_connect.create_engine())
models.Base_kws.metadata.create_all(bind=database.db_connect.create_engine(db=database.CONN_DB['kws']['db']))
models.Base_cx_sku_match.metadata.create_all(bind=database.db_connect.create_engine(server=CONN_DB['cx_sku_match']['ip'],user=CONN_DB['cx_sku_match']['user'],password=CONN_DB['cx_sku_match']['password'],port=CONN_DB['cx_sku_match']['port'],db=CONN_DB['cx_sku_match']['db']))


# 关键词连接
# Dependency
# 连接team_station
def get_db():
    session = database.SessionTeamStation()
    try:
        yield session
        session.commit()
    finally:
        session.close()

# 连接共享关键词
def get_db_kws():
    session = database.SessionKws()
    try:
        yield session
        session.commit()
    finally:
        session.close()


# 连接楚晋sku捆绑表
def get_db_cx_sku_match():
    session = database.SessionCXSKUMATCH()
    try:
        yield session
        session.commit()
    finally:
        session.close()
        
        
# 连接sku库存表数据库
def get_db_sku_inventory():
    session = database.SessionSKUINVENTORY()
    try:
        yield session
        session.commit()
    finally:
        session.close()


# 构建沃尔玛账号对象以及处理curd
walmartAccountRouter = SQLAlchemyCRUDRouter(
    schema=schema.WalmartAccount,
    create_schema=schema.WalmartAccountCreate,
    db_model=models.WalmartAccount,
    db=get_db,
    delete_all_route=False,
    delete_one_route=False,
    update_route=False,
    create_route=False,
)

# 构建关键词查询的路径对象
highQualityKwsRouter = SQLAlchemyCRUDRouter(
    schema=schema.HighQualityKeyword,
    create_schema=schema.HighQualityKeywordCreate,
    db_model=models.HighQualityKeyword,
    db=get_db_kws,
    delete_all_route=False,
    delete_one_route=False,
    update_route=False,
    create_route=False,
)


databaseRouters = APIRouter()


@databaseRouters.get('/query_kws',summary="查询共享关键词")
def query_kws(token: str,station:str=None,asin:str=None,erpsku:str=None,sku:str=None,db:Session = Depends(get_db_kws)):
    if token != static.TOKEN:
        raise HTTPException(status_code=404, detail="TOKEN ERROR")
    queryInfo = crud.query_high_quality_words(db=db,station=station,erpsku=erpsku,asin=asin,sku=sku)
    if isinstance(queryInfo,str):
        return {'msg':'fail','detail':queryInfo}
    logger.info(f'查询共享关键词.')
    return {'msg':'success','length':len(queryInfo),'data':queryInfo}


@databaseRouters.get('/cx_sku_match',summary="查询楚晋sku捆绑表")
def query_cx_sku_match(token: str,erp_sku:str=None,seller_sku:str=None,db:Session = Depends(get_db_cx_sku_match)):
    if token != static.TOKEN:
        raise HTTPException(status_code=404, detail="TOKEN ERROR")
    queryInfo = crud.query_cx_sku_match(db=db,erp_sku=erp_sku,seller_sku=seller_sku)
    if isinstance(queryInfo,str):
        return {'msg':'fail','detail':queryInfo}
    logger.info(f'查询楚晋sku捆绑表.')
    return {'msg':'success','length':len(queryInfo),'data':queryInfo}


@databaseRouters.get('/clear_sku',summary="查询清仓sku")
def clear_sku(token:str,account_name:str,db:Session = Depends(get_db)):
    if token != static.TOKEN:
        raise HTTPException(status_code=404, detail="TOKEN ERROR")
    account_id = crud.query_account_id_by_name(db=db,account_name=account_name)
    if account_id is None:
        return {'msg':'fail','detail':f'{account_name}不是有效的站点名'}
    accountClearSkuInfo = crud.query_clear_sku(db=db,account_id=account_id)
    if isinstance(accountClearSkuInfo,str):
        return {'msg':'fail','detail':f'{accountClearSkuInfo}'}
    else:
        return {'msg':'success','length':len(accountClearSkuInfo),'data':accountClearSkuInfo}


@databaseRouters.get('/sku_inventory',summary="查询站点sku库存")
def query_sku_inventory(token:str,accountNameSellerSKuInfo,limitStationNum=100,limitSKUNum=1000):
    """

    查询sku的库存量

    accountNameSellerSKuInfo是将accountName,sellerskuSku字典json化

    """
    if token != static.TOKEN:
        raise HTTPException(status_code=404, detail="TOKEN ERROR")
    if not isinstance(accountNameSellerSKuInfo,str):
        return {'msg':'fail','detail':f'查询的类型不对,{type(accountNameSellerSKuInfo)}不是str型.'}
    try:
        accountNameSellerSKuInfo = json.loads(accountNameSellerSKuInfo)
    except:
        return {'msg':'fail','detail':'查询sku库存信息的输入不是有效的json格式'}
    if not isinstance(accountNameSellerSKuInfo,dict):
        return {'msg':'fail','detail':f'查询的类型不对,{type(accountNameSellerSKuInfo)}不是字典.'}
    if len(accountNameSellerSKuInfo) > int(limitStationNum):
        return {'msg':'fail','detail':f'查询的站点个数不能超过{limitStationNum}'}
    accountIDIndexInfo = query_frequently_table_info.query_amazon_account_index()
    accountIDIndexInfoDict = {accountName:accountId for accountName,accountId in zip(accountIDIndexInfo['account_name'],accountIDIndexInfo['id'])}
    allStation = [public_function.standardStation(station) for station in accountNameSellerSKuInfo.keys()]
    accountNameSellerSKuInfo = {int(accountIDIndexInfoDict.get(public_function.standardStation(accountName))):{'name':accountName,'info':skuInfo}
                                for accountName,skuInfo in accountNameSellerSKuInfo.items()
                                if accountIDIndexInfoDict.get(public_function.standardStation(accountName),None)}
    AllInventoryDict = dict()
    for accountId,allskuInfo in accountNameSellerSKuInfo.items():
        skuInfo = allskuInfo['info']
        name = allskuInfo['name']
        if not isinstance(skuInfo,(set,list)):
            return {'msg':'fail','detail':f'查询的类型不对,查询sku信息应该是list or set not {type(skuInfo)}'}
        if len(skuInfo) > int(limitSKUNum):
            return {'msg':'fail','detail':f'单个站点的sku查询数量不能超过{limitSKUNum}.'}
        # 查询sku库存表
        AllInventoryDict[name] = query_table.sku_inventory(int(accountId),skuInfo)

    return {station:AllInventoryDict.get(station,None) for station in allStation}


@databaseRouters.get('/query_kws_by_erpsku/',summary="查询共享关键词")
def query_kws_by_erpsku(token: str,erpsku:str,page:int=1,size:int=1000,db:Session = Depends(get_db_kws)):
    if token != static.TOKEN:
        raise HTTPException(status_code=404, detail="TOKEN ERROR")
    # 选定特定的列
    chooseColumns=['station','customer_search_term','updatetime','erpsku']
    queryInfo = crud.query_high_quality_words(db=db,erpsku=erpsku,skip=page-1,pageLimit=size,chooseColumns=chooseColumns)
    if isinstance(queryInfo,str):
        return {'msg':'fail','detail':queryInfo}
    logger.info(f'查询共享关键词.')
    return {'msg':'success','length':len(queryInfo),'data':queryInfo}


# 查询erpsku 备份
@databaseRouters.get('/query_kws_by_erpsku_other/',summary="查询共享关键词")
def query_kws_by_erpsku_other(token: str,erpskuInfo:app_models.ErpSku=Body(...,embed=False),db:Session = Depends(get_db_kws)):
    if token != static.TOKEN:
        raise HTTPException(status_code=404, detail="TOKEN ERROR")
    # 选定特定的列
    erpskuInfo = erpskuInfo.dict()
    if 'erpsku' in erpskuInfo.keys():
        return {'msg':'fail','detail':'缺少必要的参数erpsku'}
    erpsku = erpskuInfo.get('erpsku')
    page = erpskuInfo.get('page',1)
    size = erpskuInfo.get('size',1000)
    chooseColumns=['station','customer_search_term','updatetime','erpsku']
    queryInfo = crud.query_high_quality_words(db=db,erpsku=erpsku,skip=page-1,pageLimit=size,chooseColumns=chooseColumns)
    if isinstance(queryInfo,str):
        return {'msg':'fail','detail':queryInfo}
    logger.info(f'查询共享关键词.')
    return {'msg':'success','length':len(queryInfo),'data':queryInfo}