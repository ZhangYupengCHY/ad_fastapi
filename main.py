#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/27 0027 9:31
# @Author  : Zhang YP
# @Email   : 1579922399@qq.com
# @github  :  Aaron Ramsey
# @File    : main.py

"""
创建广告部的api框架
"""
import logging
import os
import sys

import uvicorn
from fastapi import FastAPI, UploadFile, File, Body, Request
from pathlib import Path
from starlette.responses import FileResponse, StreamingResponse
import io
from loguru import logger

import schema
from public_function import accessManager
import static
from routers import router as api_routes
from sql_app.main import walmartAccountRouter,highQualityKwsRouter,databaseRouters
from process_dir.routes import dirRoutes
from sql_app import routes
from extensions import loggers as defaultLoggingConfig



#todo 暂时解决文档排版的问题

from fastapi import applications
from fastapi.openapi.docs import get_swagger_ui_html
def swagger_monkey_patch(*args, **kwargs):
    """
    Wrap the function which is generating the HTML for the /docs endpoint and
    overwrite the default values for the swagger js and css.
    """
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.48.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.48.0/swagger-ui.css"
    )


# Actual monkey patch
applications.get_swagger_ui_html = swagger_monkey_patch


# app的配置项
def get_application() -> FastAPI:
    application = FastAPI(title='ADApi')
    # 添加路由
    application.include_router(api_routes)
    application.include_router(walmartAccountRouter)
    # application.include_router(highQualityKwsRouter)
    application.include_router(databaseRouters)
    application.include_router(dirRoutes)
    logger.add(defaultLoggingConfig.log_path_all, rotation="12:00", retention="5 days", enqueue=True,
               level='ERROR')  # 日志等级分割
    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010, access_log=True, reload=False,
                log_config=defaultLoggingConfig.log_config)
