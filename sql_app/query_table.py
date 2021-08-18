
from sql_app.database import SessionTeamStation
from sql_app.models import *
from fastapi_sqlalchemy import db
from public_function import sql_write_read, process_file, public_function, query_frequently_table_info
from sqlalchemy.orm import Session, load_only
from datetime import datetime
import pandas as pd

from sql_app import models


def ad_amazon_all_stations(case='upper'):
    """query only station info"""
    ad_amazon_all_stations = query_frequently_table_info.query_only_station_info()
    return [public_function.standardStation(station, case=case) for station in ad_amazon_all_stations['station']]


# def query_sku_inventory(db: Session, accounID, sku):
#     # """    逻辑：
#     # afn_reserved_quantity = 0 或者  reserved_fc-transfers + reserved_fc-processing = 0的时候，转运库存 = 0
#     # 否则  转运库存 = reserved_fc-transfers + reserved_fc-processing
#     # 总可用库存 = afn_fulfillable_quantity + 转运库存 + afn_researching_quantity
#     #
#     # 其中yibai_amazon_fba_inventory_month_end表中要做筛选month = 当天,condition = New"""
#
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
#     monthlExportColumns = ['afn_reserved_quantity', 'afn_fulfillable_quantity', 'afn_researching_quantity']
#     monthlyQTY = db.query(models.YibaiAmazonFbaInventoryMonthEnd).options(load_only(*monthlExportColumns)).filter(
#         (models.YibaiAmazonFbaInventoryMonthEnd.month == nowDate) & (
#                 models.YibaiAmazonFbaInventoryMonthEnd.condition == 'New') &
#         (models.YibaiAmazonFbaInventoryMonthEnd.account_id == accounID) & (
#             models.YibaiAmazonFbaInventoryMonthEnd.sku.in_(sku))).all()
#     return rightNowQTY, monthlyQTY


def skuInventoryLogic(afn_reserved_quantity,reserved_fc_transfers,reserved_fc_processing,afn_fulfillable_quantity,afn_researching_quantity):
    """
    库存逻辑：
    afn_reserved_quantity = 0 或者  reserved_fc-transfers + reserved_fc-processing = 0的时候，转运库存 = 0
    否则  转运库存 = reserved_fc-transfers + reserved_fc-processing
    总可用库存 = afn_fulfillable_quantity + 转运库存 + afn_researching_quantity
    """
    if not isinstance(any([afn_reserved_quantity,reserved_fc_transfers,reserved_fc_processing,afn_fulfillable_quantity,afn_researching_quantity]),int):
        raise TypeError("计算库存必须是整型.")

    transforInventory = max(afn_reserved_quantity,reserved_fc_processing+reserved_fc_transfers)
    return afn_fulfillable_quantity + transforInventory + afn_researching_quantity


def sku_inventory(accounID, sku):
    """    逻辑：
    afn_reserved_quantity = 0 或者  reserved_fc-transfers + reserved_fc-processing = 0的时候，转运库存 = 0
    否则  转运库存 = reserved_fc-transfers + reserved_fc-processing
    总可用库存 = afn_fulfillable_quantity + 转运库存 + afn_researching_quantity

    其中yibai_amazon_fba_inventory_month_end表中要做筛选month = 当天,condition = New"""

    if not isinstance(accounID, int):
        return
    if not isinstance(sku, (set, list)):
        return
    if len(sku) == 0:
        return
    # 获取当前的库存信息
    exportColumns = ['sku','reserved_fc-transfers', 'reserved_fc-processing']
    rightNowSQLTable = 'yibai_amazon_reserved_inventory'

    nowDate = datetime.now().date()
    monthlyExportColumns = ['sku','afn_reserved_quantity', 'afn_fulfillable_quantity', 'afn_researching_quantity']
    monthlySQLTable = 'yibai_amazon_fba_inventory_month_end'

    skuInventorySqlInfo = {'ip': '139.9.206.7', 'port': 3306, 'user': 'wangyan', 'password': 'wyYB&^%523435',
                           'db': 'yibai_product'}
    skustr = sql_write_read.query_list_to_str(sku)
    _connMysql = sql_write_read.QueryMySQL(host=skuInventorySqlInfo['ip'], port=skuInventorySqlInfo['port'],
                                           username=skuInventorySqlInfo['user'],
                                           password=skuInventorySqlInfo['password'], database=skuInventorySqlInfo['db'])
    # 读取sku库存表
    rightNowQTYSQL = """select `sku`,`reserved_fc-transfers`,`reserved_fc-processing` from `%s` where `account_id` = %s and sku in (%s)""" % (
    rightNowSQLTable, accounID, skustr)
    monthlyQTYSQL = """select `sku`,`afn_reserved_quantity`,`afn_fulfillable_quantity`,`afn_researching_quantity` from `%s` where (`condition` = 'New') and (`month` = '%s') and (`sku` in (%s)) and (`account_id` = %s) """ %(monthlySQLTable,nowDate,skustr,accounID)
    rightNowInfo = _connMysql.read_table(rightNowSQLTable,rightNowQTYSQL,columns=exportColumns)
    monthlyInfo = _connMysql.read_table(monthlySQLTable,monthlyQTYSQL,columns=monthlyExportColumns)
    _connMysql.close()

    if (rightNowInfo is None) or (rightNowInfo.empty):
        rightNowInfo = pd.DataFrame([sku,[0]*len(sku),[0]*len(sku)]).T
        rightNowInfo.columns= exportColumns
    if (monthlyInfo is None) or (monthlyInfo.empty):
        monthlyInfo = pd.DataFrame([sku,[0]*len(sku),[0]*len(sku),[0]*len(sku)]).T
        monthlyInfo.columns= monthlyExportColumns
    #
    skuInventoryInfo = pd.merge(rightNowInfo,monthlyInfo,on='sku',how='inner')
    skuInventoryDict = {}
    for sku_ in skuInventoryInfo['sku']:
        oneSkuInventoryInfo =  skuInventoryInfo[skuInventoryInfo['sku'] == sku_]
        skuInventoryDict[sku_] = skuInventoryLogic(int(oneSkuInventoryInfo['afn_reserved_quantity'].values[0]),
                                                  int(oneSkuInventoryInfo['reserved_fc-transfers'].values[0]),
                                                  int(oneSkuInventoryInfo['reserved_fc-processing'].values[0]),
                                                  int(oneSkuInventoryInfo['afn_fulfillable_quantity'].values[0]),
                                                  int(oneSkuInventoryInfo['afn_researching_quantity'].values[0]))
    return {oneSku:skuInventoryDict.get(oneSku,None) for oneSku in sku}



if __name__ == '__main__':
    print(sku_inventory(107,['CHE-ZMX--JM27639FBA','CYMZEUJYA01920-170614']))