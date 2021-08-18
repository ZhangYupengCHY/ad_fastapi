#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/6 0006 17:35
# @Author  : Zhang YP
# @Email   : 1579922399@qq.com
# @github  :  Aaron Ramsey
# @File    : main.py
import os
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Body,APIRouter,HTTPException
from starlette.responses import FileResponse, StreamingResponse
import json


import static
import schema
from public_function import accessManager,public_function
from loguru import logger
from sql_app import query_table

router = APIRouter()


@router.get('/')
def home():
    logger.info('visit homepage.')
    return 'WELCOME TO ADapi'


@router.get("/download_station_folder", summary="下载五表")
async def download_station_folder(token: str, station: schema.stationRequest):
    # 处理下载文件
    if token != static.TOKEN:
        raise HTTPException(status_code=404, detail="INVALID TOKEN")
    # 站点文件保存的地址
    stationFolder = static.REMOTEFIVEFILESSAVEFOLDER
    stationDict = json.loads(station.json())
    if 'station' not in stationDict:
        return {'msg':'error','detail':'请求参数station不存在'}
    requestStation = stationDict.get('station')
    requestStation  =public_function.standardStation(requestStation,case='lower')
    # 判断文件存不存在
    filePath = os.path.join(stationFolder,f"{requestStation}.zip")
    logger.info(f'下载{requestStation}')
    if not os.path.exists(filePath):
        return {'msg':'error','detail':f'{requestStation}五表压缩包不存在.'}
    else:
        return FileResponse(filePath)


@router.get("/upload_station_folder", summary="上传五表")
async def upload_station_folder(token: str,  upload_file: UploadFile = File(...)):
    # 处理上传文件
    if token != static.TOKEN:
        raise HTTPException(status_code=404, detail="TOKEN ERROR")
    # 处理逻辑
    stationBaseName = upload_file.filename
    stationBaseName = public_function.standardStation(stationBaseName,case='upper')
    stationName = os.path.splitext(stationBaseName)[0]
    # 判断站点名是否有效
    if len(stationName) < 3:
        return {'msg': 'fail', 'detail': f"上传的文件名{stationName}无效."}
    site = stationName[-2:].upper()
    if site not in static.CN_EN_SITE_DICT.values():
        return {'msg': 'fail', 'detail': f"上传的站点名{site}无效."}
    # 判断上传的站点是否有效
    if stationName not in query_table.ad_amazon_all_stations():
        return {'msg': 'fail', 'detail': f"上传的站点名{stationName}暂时还未接手."}
    logger.info(f'上传{stationName}')
    saveFolder = static.STATIONFIVEFILESSAVEFOLDER
    savePath = os.path.join(saveFolder,f'{stationName}.zip')
    if os.path.exists(savePath):
        os.remove(savePath)
    with open(savePath, 'wb+') as f:
        f.write(upload_file.file.read())  # async write
    return {'msg': 'success','file':upload_file.filename}


@router.get('/upload_upload_file',summary='上传上传表')
async def upload_upload_file(token: str,  upload_file: UploadFile = File(...)):
    # 处理上传文件
    if token != static.TOKEN:
        raise HTTPException(status_code=404, detail="TOKEN ERROR")
    # 处理逻辑
    uploadFileName = upload_file.filename
    uploadFileInfo,uploadFileType = os.path.splitext(uploadFileName)
    # 判断输入文件类型
    if uploadFileType.lower() != '.xlsx':
        return {'msg': 'fail', 'detail': f"上传的文件类型{uploadFileType}无效."}
    # 上传表的格式为 日期 站点名 upload
    uploadFileInfo = uploadFileInfo.split(' ')
    if len(uploadFileInfo) != 3:
        return {'msg': 'fail', 'detail': f"上传的文件格式{uploadFileName}有问题."}
    uploadFileNameDate = uploadFileInfo[0]
    uploadFileNameFormat = '%y.%m.%d'
    try:
        datetime.strptime(uploadFileNameDate,uploadFileNameFormat)
    except:
        return {'msg': 'fail', 'detail': f"上传的文件日期标识有问题,应该类似为:21.09.21"}
    # 判断站点名是否有效
    uploadStationName = uploadFileInfo[1]
    uploadStationName = public_function.standardStation(uploadStationName,case='upper')
    if uploadStationName not in query_table.ad_amazon_all_stations(case='upper'):
        return {'msg': 'fail', 'detail': f"上传的站点名{uploadStationName}暂时还未接手."}
    # 判断结尾是否是upload
    uploadSignWord = 'upload'
    if uploadFileInfo[2] != uploadSignWord:
        return {'msg': 'fail', 'detail': f"上传表结尾应该为:{uploadSignWord}"}
    logger.info(f'上传上传表{uploadStationName}')
    saveFolder = static.UPLOADFILESAVEFOLDER
    uploadStandardFileName = f'{uploadFileNameDate} {uploadStationName} {uploadSignWord}.xlsx'
    savePath = os.path.join(saveFolder,uploadStandardFileName)
    # 删除本站点的上传表信息
    try:
        [os.remove(os.path.join(saveFolder,file)) for file in os.listdir(saveFolder) if uploadStationName in file]
    except Exception as e:
        return {'msg': 'fail', 'detail': f"删除站点{uploadStationName}历史表失败,原因{e}."}
    # 写入上传表
    with open(savePath, 'wb+') as f:
        f.write(upload_file.file.read())  # async write
    return {'msg': 'success','file':upload_file.filename}


@router.get('/getToken', summary="获取token")
def get_token(iss: str, secret: str):
    # 获取token
    requestCode = iss + secret
    token = accessManager.hash_code(requestCode)
    return {'token': token}