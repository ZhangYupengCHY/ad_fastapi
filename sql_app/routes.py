from fastapi_crudrouter import DatabasesCRUDRouter as CRUDRouter

from sql_app.models import HighQualityKeyword

# router = CRUDRouter(model=HighQualityKeyword)
#
#
# @router.get('')
# def overloaded_get_all():
#     return 'My overloaded route that returns all the items'