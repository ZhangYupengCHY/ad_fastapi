import io
import json

from fastapi import APIRouter,Depends,HTTPException,FastAPI, UploadFile, File,Body,Response
import os
from starlette.responses import FileResponse,StreamingResponse
import io
from loguru import logger
import pandas as pd
import pickle as pickle


from public_function import process_file
from public_function.response_message import Message
from sql_app import models as app_models


dirRoutes = APIRouter()


@dirRoutes.get('/dirlist/')
def dirs_list(dir_path:app_models.Path=Body(...,embed=False)):
    """获服务器文件夹目录"""
    path = dir_path.dict()['path']
    path = json.loads(path)
    if isinstance(path, str):
        if not os.path.exists(path):
            return Message.folder_not_exist(path)
        else:
            if os.path.isdir(path):
                return os.listdir(path)
            else:
                return Message.error_msg(f'{path} not a folder.')
    elif isinstance(path,(set,list)):
        return {one_path:os.listdir(one_path) if (os.path.exists(one_path)) & (os.path.isdir(one_path)) else None for one_path in path}


@dirRoutes.get('/file_exist/')
def file_exist(file_path:app_models.Path=Body(...,embed=False)):
    """判断文件是否存在"""
    path = file_path.dict()['path']
    path = json.loads(path)
    if isinstance(path,str):
        return os.path.exists(path)
    else:
        return {one_path:os.path.exists(one_path) for one_path in path}

@dirRoutes.get('/is_dir/')
def is_dir(dir_path:app_models.Path=Body(...,embed=False)):
    """获服务器文件夹目录"""
    path = dir_path.dict()['path']
    path = json.loads(path)
    if isinstance(path, str):
        if not os.path.isdir(path):
            return False
        else:
            return True
    elif isinstance(path,(set,list)):
        return {one_path:True if os.path.isdir(one_path) else False for one_path in path}


@dirRoutes.get('/make_dir/')
def make_dir(path:app_models.Path=Body(...,embed=False)):
    path = path.dict()['path']
    path = json.loads(path)
    if isinstance(path,str):
        if not os.path.exists(path):
            os.mkdir(path)
        return Message.success()
    if isinstance(path,(list,set)):
        {os.mkdir(one_path) if not os.path.exists(one_path) else None for one_path in path}
        return Message.success()


@dirRoutes.get('/download_file/')
def download_file(file_path):
    """下载文件"""
    if not os.path.exists(file_path):
        return Message.folder_not_exist(file_path)
    else:
        return FileResponse(file_path)


@dirRoutes.get('/read_file/')
def read_file(file_path,type='r'):
    """下载文件"""
    if not os.path.exists(file_path):
        return Message.folder_not_exist(file_path)
    else:
        if type == 'rb':
            return Response(process_file.read_file_as_bytes(file_path))
        elif type == 'r':
            for encodingType in ['gbk','utf-8']:
                try:
                    with open(file_path,'r+', encoding=encodingType) as f:
                        data = f.read()
                    return data
                except:
                    continue
            return Message.error_msg(f'cant read {file_path}')


@dirRoutes.get('/read_excel/')
def read_excel(path:app_models.Path=Body(...,embed=False)):
    path = path.dict()['path']
    path = json.loads(path)
    if isinstance(path, str):
        if os.path.exists(path):
            return Response(pickle.dumps(process_file.read_excel(path)))
    if isinstance(path, (list, set)):
        pathDf = {onePath:process_file.read_excel(onePath) for onePath in path}
        pathDfJson = {path:pathDf.to_json() if isinstance(pathDf,pd.DataFrame) else json.dumps({'error':'excel read error'}) for path,pathDf in pathDf.items()}
        return Response(json.dumps(pathDfJson).encode())


@dirRoutes.post('/upload_file/')
def upload_file(savePath,fileBytes:bytes=File(...)):
    saveFolder = os.path.dirname(savePath)
    if not os.path.exists(saveFolder):
        os.mkdir(saveFolder)
    with open(savePath,'wb') as f:
        f.write(fileBytes)
    logger.info(f'销售上传{os.path.basename(savePath)}')


@dirRoutes.post('/upload_folder/')
def upload_folder(folderPath,fileBytes:bytes=File(...)):
    savepath = os.path.join(os.path.dirname(folderPath),os.path.basename(folderPath)+'.zip')
    with open(savepath,'wb') as f:
        f.write(fileBytes)


@dirRoutes.get('/delete_file/')
def delete_file(path:app_models.Path=Body(...,embed=False)):
    path = path.dict()['path']
    path = json.loads(path)
    if isinstance(path, str):
        if os.path.exists(path):
            os.remove(path)
        return Message.success()
    if isinstance(path, (list, set)):
        {os.remove(one_path) if os.path.exists(one_path) else None for one_path in path}
        return Message.success()


@dirRoutes.get('/fileTime/')
def file_time(path:app_models.Path=Body(...,embed=False)):
    path = path.dict()['path']
    path = json.loads(path)
    if isinstance(path,str):
        if os.path.exists(path):
            return process_file.file_modify_time(path)
        else:
            return
    if isinstance(path,(list,set)):
        return {one_path:process_file.file_modify_time(one_path) if os.path.exists(one_path) else None for one_path in path}


