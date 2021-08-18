#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/7 0007 16:53
# @Author  : Zhang YP
# @Email   : 1579922399@qq.com
# @github  :  Aaron Ramsey
# @File    : models.py

"""
模型设计
"""

from sqlalchemy import Column, Integer, String, DateTime,Text,Float,TIMESTAMP,text,CHAR,DECIMAL,Date
from sqlalchemy.dialects.mysql import BIGINT,INTEGER,TINYINT,VARCHAR,SMALLINT,MEDIUMINT
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()
Base_kws = declarative_base()
Base_cx_sku_match = declarative_base()
Base_cx_sku_inventory = declarative_base()


class WalmartAccount(Base):
    """
    walmart全部的账号信息
    """
    __tablename__ = 'walmart_account'
    id = Column(BIGINT(20), primary_key=True)
    account = Column(Text)
    updatetime = Column(DateTime)


class OnlyStationInfo(Base):
    """广告站点实时基本表现信息"""
    __tablename__ = 'only_station_info'

    id = Column(BIGINT(20))
    station = Column(Text, nullable=False)
    company = Column(Text, nullable=False)
    owner = Column(Text)
    operator = Column(Text)
    ad_manger = Column(Text)
    content = Column(Text)
    acos = Column(Text)
    ad_sales = Column(Float(asdecimal=True), comment='本币')
    percentage = Column(Float(10))
    accept_time = Column(Text)
    operator_time = Column(Text)
    update_time = Column(Text)
    shop_sales = Column(Float(asdecimal=True))
    cpc = Column(Float(asdecimal=True))
    note = Column(Text)
    give_other_time = Column(Text)
    rowid = Column(INTEGER(10), primary_key=True)


class HighQualityKeyword(Base_kws):
    __tablename__ = 'high_quality_keywords'

    id = Column(BIGINT(20), primary_key=True)
    station = Column(String(128, 'utf8_unicode_ci'))
    erpsku = Column(String(255, 'utf8_unicode_ci'))
    asin = Column(String(128, 'utf8_unicode_ci'))
    sku = Column(String(128, 'utf8_unicode_ci'))
    campaign_name = Column(Text(collation='utf8_unicode_ci'))
    ad_group_name = Column(Text(collation='utf8_unicode_ci'))
    match_type = Column(Text(collation='utf8_unicode_ci'))
    customer_search_term = Column(Text(collation='utf8_unicode_ci'))
    impression = Column(BIGINT(20))
    click = Column(BIGINT(20))
    spend = Column(Float(asdecimal=True))
    sale = Column(Float(asdecimal=True))
    order = Column(BIGINT(20))
    ctr = Column(Text(collation='utf8_unicode_ci'))
    cpc = Column(Float(asdecimal=True))
    acos = Column(Text(collation='utf8_unicode_ci'))
    cr = Column(Text(collation='utf8_unicode_ci'))
    sku_sale = Column(Float(asdecimal=True))
    item_name = Column(Text(collation='utf8_unicode_ci'))
    kws_lang = Column(String(20, 'utf8_unicode_ci'))
    updatetime = Column(DateTime)
    keyword_1 = Column(String(128, 'utf8_unicode_ci'))
    keyword_2 = Column(String(128, 'utf8_unicode_ci'))
    keyword_3 = Column(String(128, 'utf8_unicode_ci'))
    keyword_4 = Column(String(128, 'utf8_unicode_ci'))
    keyword_5 = Column(String(128, 'utf8_unicode_ci'))
    keyword_6 = Column(String(128, 'utf8_unicode_ci'))
    keyword_7 = Column(String(128, 'utf8_unicode_ci'))
    keyword_8 = Column(String(128, 'utf8_unicode_ci'))
    keyword_9 = Column(String(128, 'utf8_unicode_ci'))
    keyword_10 = Column(String(128, 'utf8_unicode_ci'))


class YibaiAmazonSkuMap(Base):
    __tablename__ = 'yibai_amazon_sku_map'

    id = Column(INTEGER(10), primary_key=True)
    seller_sku = Column(VARCHAR(128))
    sku = Column(VARCHAR(255))
    owner = Column(INTEGER(11))
    owner_name = Column(VARCHAR(80))
    account_id = Column(INTEGER(11))
    account_name = Column(VARCHAR(80))
    saler_name = Column(String(80, 'utf8_unicode_ci'), server_default=text("''"), comment='销售负责人姓名')
    saler = Column(INTEGER(11), comment='销售负责人id')
    assit = Column(INTEGER(11))
    assit_name = Column(String(80, 'utf8_unicode_ci'))
    status = Column(TINYINT(4), comment='数据来源:2-表格导入,3-系统导入,4-手动添加,5-手动编辑,6-从异常订单录入,7-自动转FBA,9-从listing管理表同步')
    create_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    seller_sku2 = Column(VARCHAR(128))
    update_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    deliver_mode = Column(SMALLINT(6), server_default=text("'0'"), comment='发货模式')
    type = Column(SMALLINT(6), server_default=text("'0'"), comment='1fba范欧，2fbm欧洲，3fbm北美，4fba北美')
    saler_type = Column(SMALLINT(6), server_default=text("'0'"), comment='是否直接获取匹配捆绑表销售名称1：是 0：否')


class ClearSku(Base):
    """清仓sku表"""
    __tablename__ = 'clear_sku'

    id = Column(INTEGER(10), primary_key=True, comment='虚拟主键,无实际意义')
    account_id = Column(MEDIUMINT(6), comment='店铺id')
    clear_sku = Column(String(255), comment='清仓sku')
    erp_sku = Column(String(255), comment='erp-sku')
    stock_num = Column(MEDIUMINT(8), comment='库存数量')
    start_time = Column(DateTime, comment='开始变成清仓的时间')
    redundant_days = Column(MEDIUMINT(5), comment='冗余天数')
    sale_status = Column(String(255), comment='销售状态')
    price = Column(Float(15), comment='目前售价')
    _30_sales = Column('30_sales', Float(15), comment='近30天销售额')
    _30_orders = Column('30_orders', INTEGER(10), comment='近30天销售数量')
    update_time = Column(DateTime)


class AccountIdIndex(Base):
    __tablename__ = 'account_id_index'

    id = Column(MEDIUMINT(9), primary_key=True)
    account_name = Column(String(255))
    update_time = Column(DateTime)


class YibaiAmazonReservedInventory(Base_cx_sku_inventory):
    """sku库存表1"""
    __tablename__ = 'yibai_amazon_reserved_inventory'
    __table_args__ = {'comment': '亚马逊库存表'}

    id = Column(INTEGER(10), primary_key=True)
    account_id = Column(INTEGER(10), server_default=text("'0'"), comment='账号id')
    account_name = Column(CHAR(50), server_default=text("''"))
    asin = Column(CHAR(20), server_default=text("''"))
    fnsku = Column(String(120), server_default=text("''"))
    sku = Column(String(120), server_default=text("''"))
    product_name = Column(String(320), server_default=text("''"))
    reserved_customerorders = Column(INTEGER(10), server_default=text("'0'"))
    reserved_fc_transfers = Column('reserved_fc-transfers', INTEGER(10), server_default=text("'0'"))
    reserved_fc_processing = Column('reserved_fc-processing', INTEGER(10), server_default=text("'0'"))
    reserved_qty = Column(INTEGER(10), server_default=text("'0'"))
    create_date = Column(DateTime, server_default=text("'0000-00-00 00:00:00'"), comment='创建时间')


class YibaiAmazonFbaInventoryMonthEnd(Base_cx_sku_inventory):
    """sku库存表2"""
    __tablename__ = 'yibai_amazon_fba_inventory_month_end'

    id = Column(INTEGER(11), primary_key=True)
    account_id = Column(INTEGER(11))
    month = Column(Date)
    sku = Column(String(80), server_default=text("''"), comment='seller sku !!!')
    fnsku = Column(String(20), server_default=text("''"))
    asin = Column(String(20), server_default=text("''"))
    product_name = Column(String(255), server_default=text("''"))
    short_product_name = Column(String(255), server_default=text("''"))
    image_url = Column(String(255), server_default=text("''"))
    condition = Column(String(80), server_default=text("''"))
    your_price = Column(DECIMAL(10, 2), server_default=text("'0.00'"), comment='价格')
    mfn_listing_exists = Column(String(4), server_default=text("''"), comment='卖家自配送商品(YES 或 空值)')
    mfn_fulfillable_quantity = Column(INTEGER(11), server_default=text("'0'"), comment='卖家自配送可售数量')
    afn_listing_exists = Column(String(4), server_default=text("''"), comment='亚马逊配送商品(YES 或 空值)')
    afn_warehouse_quantity = Column(INTEGER(11), server_default=text("'0'"), comment='亚马逊库存数量')
    afn_fulfillable_quantity = Column(INTEGER(11), server_default=text("'0'"), comment='亚马逊物流可售数量')
    afn_unsellable_quantity = Column(INTEGER(11), server_default=text("'0'"), comment='亚马逊物流不可售数量')
    afn_reserved_quantity = Column(INTEGER(11), server_default=text("'0'"), comment='亚马逊物流预留数量')
    afn_total_quantity = Column(INTEGER(11), server_default=text("'0'"), comment='亚马逊物流总数量')
    per_unit_volume = Column(DECIMAL(10, 2), server_default=text("'0.00'"), comment='商品单位体积')
    afn_inbound_working_quantity = Column(INTEGER(11), server_default=text("'0'"), comment='亚马逊物流入库处理数量')
    afn_inbound_shipped_quantity = Column(INTEGER(11), server_default=text("'0'"), comment='亚马逊物流入库发货数量')
    afn_inbound_receiving_quantity = Column(INTEGER(11), server_default=text("'0'"), comment='亚马逊物流入库接收数量')
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    open_date = Column(DateTime, server_default=text("'0000-00-00 00:00:00'"), comment='listing_alls表open_date')
    md5_check = Column(String(32), comment='m5对account_id,sku,asin,fnsku进行校验')
    afn_researching_quantity = Column(INTEGER(11), server_default=text("'0'"), comment='亚马逊调研数量')
    afn_reserved_future_supply = Column(INTEGER(11), server_default=text("'0'"), comment='亚马逊物流-网络预留未来供货')
    afn_future_supply_buyable = Column(INTEGER(11), server_default=text("'0'"), comment='亚马逊物流-网络未来可购买供货')


class Path(BaseModel):
    path:str


class Station(BaseModel):
    station:str