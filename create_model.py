from urllib import parse
import os

tableName = 'yibai_amazon_fba_inventory_month_end'


ret = os.popen(
    # f"sqlacodegen --noviews --noconstraints --noindexes --tables {tableName} mysql://marmot:marmot123@wuhan.yibai-it.com:33061/team_station?charset=utf8"
    f"sqlacodegen --noviews --noconstraints --noindexes --tables {tableName} mysql://wangyan:{parse.quote_plus('wyYB&^%523435')}@139.9.206.7:3306/yibai_product?charset=utf8"
    # f"sqlacodegen --noviews --noconstraints --noindexes --tables {tableName} mysql://wangyan:wyYB&^%523435@139.9.206.7:3306/yibai_product?charset=utf8"
)
print(ret.read())