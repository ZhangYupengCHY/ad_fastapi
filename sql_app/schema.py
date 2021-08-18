#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/8 0008 9:33
# @Author  : Zhang YP
# @Email   : 1579922399@qq.com
# @github  :  Aaron Ramsey
# @File    : schema.py


from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AccountId(BaseModel):
    id: int


class requestLimit(BaseModel):
    limit: int


class WalmartAccountCreate(BaseModel):
    account: str
    updatetime: datetime


class WalmartAccount(WalmartAccountCreate):
    """
    walmart账号
    """
    id: int

    class Config:
        orm_mode = True


class HighQualityKeywordCreate(BaseModel):
    station: Optional[str] = None
    erpsku: Optional[str] = None
    asin: Optional[str] = None
    sku: Optional[str] = None
    campaign_name: Optional[str] = None
    ad_group_name: Optional[str] = None
    match_type: Optional[str] = None
    customer_search_term: Optional[str] = None
    impression: Optional[int] = None
    click: Optional[int] = None
    spend: Optional[float] = None
    sal: Optional[float] = None
    order: Optional[int] = None
    ctr: Optional[str] = None
    cpc: Optional[float] = None
    acos: Optional[str] = None
    cr: Optional[str] = None
    sku_sale: Optional[float] = None
    item_name: Optional[str] = None
    kws_lang: Optional[str] = None
    updatetime: Optional[datetime] = None
    keyword_1: Optional[str] = None
    keyword_2: Optional[str] = None
    keyword_3: Optional[str] = None
    keyword_4: Optional[str] = None
    keyword_5: Optional[str] = None
    keyword_6: Optional[str] = None
    keyword_7: Optional[str] = None
    keyword_8: Optional[str] = None
    keyword_9: Optional[str] = None
    keyword_10: Optional[str] = None


class HighQualityKeyword(HighQualityKeywordCreate):
    """
    共享关键词
    """
    id: int

    class Config:
        orm_mode = True
