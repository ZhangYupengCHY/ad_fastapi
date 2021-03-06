"""
查询数据库中经常需要的信息
"""

from public_function.sql_write_read import QueryDatabaseFrequentlyInfo



def query_company_organization(companyOrgTable='company_organization',
                               columns=['user_number', 'department_name','job_name', 'pos_name', 'dep_path'],
                               redis_expire_time=3600):
    """
    查询公司组织架构
    """
    if (columns is not None) and (not isinstance(columns, (set, list))):
        raise TypeError('query company organization columns type must list or set}')
    _connDb = QueryDatabaseFrequentlyInfo(companyOrgTable, columns=columns, redis_interval_updatetime=redis_expire_time)
    return _connDb.read_table_info()


def query_seller_stations(sellerStationsTable='erp_seller_account', columns=['part','group','name','job_number', 'short_name'],
                          redis_expire_time=5*60):
    """
    查询销售负责的站点信息
    """
    if (columns is not None) and (not isinstance(columns, (set, list))):
        raise TypeError('erp_seller_account columns type must list or set}')
    _connDb = QueryDatabaseFrequentlyInfo(sellerStationsTable, columns=columns,
                                          redis_interval_updatetime=redis_expire_time)
    return _connDb.read_table_info()


def query_seller_name_bridge(sellerNameBridgeTable='nickname', columns=['work_number', 'real_name', 'nickname'],
                             redis_expire_time=24 * 3600):
    """
    查询销售负责的站点信息
    """
    if (columns is not None) and (not isinstance(columns, (set, list))):
        raise TypeError('query company organization columns type must list or set}')
    _connDb = QueryDatabaseFrequentlyInfo(sellerNameBridgeTable, columns=columns,
                                          redis_interval_updatetime=redis_expire_time)
    return _connDb.read_table_info()


def query_aliexpress_account_info(aliexpressAccountInfoTable='ali_express_account', columns=None,
                                  redis_expire_time=24 * 3600):
    """
    查询速卖通中账号信息
    """
    if (columns is not None) and (not isinstance(columns, (set, list))):
        raise TypeError('query aliexpress account columns type must list or set}')
    _connDb = QueryDatabaseFrequentlyInfo(aliexpressAccountInfoTable, columns=columns,
                                          redis_interval_updatetime=redis_expire_time)
    return _connDb.read_table_info()


def query_aliexpress_account_current_perf(sqlTable='ali_express_ad_current_perf', columns=None,
                                          redis_expire_time=5 * 60):
    """
    查询速卖通账号当前的表现
    :return:
    """
    if (columns is not None) and (not isinstance(columns, (set, list))):
        raise TypeError('query aliexpress account current columns type must list or set}')
    _connDb = QueryDatabaseFrequentlyInfo(sqlTable, columns=columns, redis_interval_updatetime=redis_expire_time)
    return _connDb.read_table_info()


def query_account_index(sqlTable='ali_express_ad_current_perf', columns=None,
                                          redis_expire_time=5 * 60):
    """
    查询速卖通账号当前的表现
    :return:
    """
    if (columns is not None) and (not isinstance(columns, (set, list))):
        raise TypeError('query aliexpress account current columns type must list or set}')
    _connDb = QueryDatabaseFrequentlyInfo(sqlTable, columns=columns, redis_interval_updatetime=redis_expire_time)
    return _connDb.read_table_info()


def query_amazon_account_index(sqlTable='account_id_index', columns=None,
                                          redis_expire_time=12 * 3600):
    """
    查询亚马逊当前账号
    :return:
    """
    if (columns is not None) and (not isinstance(columns, (set, list))):
        raise TypeError('query amazon account current columns type must list or set}')
    _connDb = QueryDatabaseFrequentlyInfo(sqlTable, columns=columns, redis_interval_updatetime=redis_expire_time)
    return _connDb.read_table_info()


def query_amazon_account_short_name(sqlTable='account_short_name', columns=None,
                                          redis_expire_time=12 * 3600):
    """
    查询亚马逊当前账号
    :return:
    """
    if (columns is not None) and (not isinstance(columns, (set, list))):
        raise TypeError('query account_short_name columns type must list or set}')
    _connDb = QueryDatabaseFrequentlyInfo(sqlTable, columns=columns, redis_interval_updatetime=redis_expire_time)
    return _connDb.read_table_info()


def query_yibai_amazon_account_status(sqlTable='account_status', columns=None,
                                          redis_expire_time=12 * 3600):
    """
    查询亚马逊当前账号
    :return:
    """
    if (columns is not None) and (not isinstance(columns, (set, list))):
        raise TypeError('account_status type must list or set}')
    _connDb = QueryDatabaseFrequentlyInfo(sqlTable, columns=columns, redis_interval_updatetime=redis_expire_time)
    return _connDb.read_table_info()


def query_cj_amazon_account(sqlTable='cj_amazon_account', columns=None,
                                          redis_expire_time=12 * 3600):
    """
    查询亚马逊当前账号
    :return:
    """
    if (columns is not None) and (not isinstance(columns, (set, list))):
        raise TypeError('cj_amazon_account type must list or set}')
    _connDb = QueryDatabaseFrequentlyInfo(sqlTable, columns=columns, redis_interval_updatetime=redis_expire_time)
    return _connDb.read_table_info()


def query_remote_request_monthly_br(sqlTable='station_monthly_data_br', columns=None,
                                          redis_expire_time=12 * 3600 * 10):
    """
    查询远程请求br月数据报表
    :return:
    """
    if (columns is not None) and (not isinstance(columns, (set, list))):
        raise TypeError('station_monthly_data_br type must list or set}')
    _connDb = QueryDatabaseFrequentlyInfo(sqlTable, columns=columns, redis_interval_updatetime=redis_expire_time)
    return _connDb.read_table_info()


def query_amazon_ad_api_auth(sqlTable='user_code', db='ad_db',columns=None,
                                          redis_expire_time= 3600):
    """
    查询远程请求br月数据报表
    :return:
    """
    if (columns is not None) and (not isinstance(columns, (set, list))):
        raise TypeError('user_code columns type must list or set}')
    _connDb = QueryDatabaseFrequentlyInfo(sqlTable, mysql_db=db,columns=columns, redis_interval_updatetime=redis_expire_time)
    return _connDb.read_table_info()



def query_only_station_info(sqlTable='only_station_info',columns=None,
                                          redis_expire_time= 10*60):
    """
    查询当前站点报表
    :return:
    """
    if (columns is not None) and (not isinstance(columns, (set, list))):
        raise TypeError('only_station_info columns type must list or set}')
    _connDb = QueryDatabaseFrequentlyInfo(sqlTable,columns=columns, redis_interval_updatetime=redis_expire_time)
    return _connDb.read_table_info()



def query_station_statistic(sqlTable='station_statistic',columns=None,
                                          redis_expire_time= 24*3600):
    """
    查询月数据
    :return:
    """
    if (columns is not None) and (not isinstance(columns, (set, list))):
        raise TypeError('station_statistic columns type must list or set}')
    _connDb = QueryDatabaseFrequentlyInfo(sqlTable,columns=columns, redis_interval_updatetime=redis_expire_time)
    return _connDb.read_table_info()


def query_station_brand_advertising_info(sqlTable='station_brand_advertising_info',columns=None,
                                          redis_expire_time= 10*60):
    """
    查询站点品牌广告表现
    :return:
    """
    if (columns is not None) and (not isinstance(columns, (set, list))):
        raise TypeError('station_brand_advertising_info columns type must list or set}')
    _connDb = QueryDatabaseFrequentlyInfo(sqlTable,columns=columns, redis_interval_updatetime=redis_expire_time)
    return _connDb.read_table_info()


def query_station_primary_listing(sqlTable='station_primary_listing',columns=None,
                                          redis_expire_time= 2*3600):
    """
    查询站点重点list
    :return:
    """
    if (columns is not None) and (not isinstance(columns, (set, list))):
        raise TypeError('station_primary_listing columns type must list or set}')
    _connDb = QueryDatabaseFrequentlyInfo(sqlTable,columns=columns, redis_interval_updatetime=redis_expire_time)
    return _connDb.read_table_info()


def query_same_ad_station_total_new(sqlTable='same_ad_station_total_new',columns=None,
                                          redis_expire_time= 2*3600):
    """
    查询重复广告
    :return:
    """
    if (columns is not None) and (not isinstance(columns, (set, list))):
        raise TypeError('same_ad_sku_total_new columns type must list or set}')
    _connDb = QueryDatabaseFrequentlyInfo(sqlTable,columns=columns, redis_interval_updatetime=redis_expire_time)
    return _connDb.read_table_info()


def query_access_seller_search_sku_performance(sqlTable='access_seller_search_sku_performance',columns=None,
                                          redis_expire_time= 24*3600):
    """
    权限分配查询广告报表中sku表现
    :return:
    """
    if (columns is not None) and (not isinstance(columns, (set, list))):
        raise TypeError('access_seller_search_sku_performance columns type must list or set}')
    _connDb = QueryDatabaseFrequentlyInfo(sqlTable,columns=columns, redis_interval_updatetime=redis_expire_time)
    return _connDb.read_table_info()



def query_other_company_belong(sqlTable='other_company_belong',columns=None,
                                          redis_expire_time= 24*3600):
    """
    查询外公司全部信息
    :return:
    """
    if (columns is not None) and (not isinstance(columns, (set, list))):
        raise TypeError('other_company_belong columns type must list or set}')
    _connDb = QueryDatabaseFrequentlyInfo(sqlTable,columns=columns, redis_interval_updatetime=redis_expire_time)
    return _connDb.read_table_info()


