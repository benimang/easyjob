#coding=utf-8

from enum import Enum
import hashlib
import os

from core.data import GlobalData
from core.utils.fileUtils import delFile
from core.utils.httpUtil import httpGet
from core.utils.traceUtil import traceYellow, traceRed, trace
from core.utils.zipUtil import decompress
from core.version import VersionFile


class UpdateManager():
    
    def __init__(self):
        self._enabled = True
        self._localVersion = VersionFile('localDeploy')
        self._serverVersion = VersionFile('serverDeploy')
        self._downloadUrl = ''
    
    def setEnabled(self, value):
        self._enabled = value
        
    def getEnabled(self):
        return self._enabled
    
    def init(self, serverDeployUrl, downloadUrl):
        self._serverVersion.resetByUrl(serverDeployUrl)
        self._downloadUrl = downloadUrl

    def updateFile(self, file):
        if not self._enabled:
            traceYellow('忽略检查文件更新 {0}'.format(file))
            return UpdateStatus.IGNORE
        localVersion = self._localVersion.getFileVersion(file)
        serverVersion = self._serverVersion.getFileVersion(file)
        if serverVersion == None:
            traceRed('检查文件更新失败（指定文件未部署） ' + file)
            return UpdateStatus.NOT_DEPLOY
        elif localVersion == serverVersion:
            trace('检查文件完成（无需更新） ' + file)
            return UpdateStatus.LASTEST
        else:
            trace('开始下载更新文件 ' + file)
            # 整理需要下载的文件
            downloadList = []
            if len(serverVersion) == 1:
                downloadList.append([file, serverVersion[0]])
            else:
                i = 0
                for md5 in serverVersion:
                    downloadList.append([file+'.%03d'%i, md5])
                    i += 1
            tempFolder = os.path.join(GlobalData.rootFolder, '__temp')
            # 下载文件
            for subFile, md5 in downloadList:
                content = httpGet(self._downloadUrl + subFile)
                if hashlib.md5(content) != md5:
                    trace('更新失败')
                    return UpdateStatus.LOAD_FAILURE
                    break
                with open(os.path.join(tempFolder, os.path.basename(subFile)), 'wb') as f:
                    f.write(content)
            # 解压缩文件
            decompress(os.path.join(GlobalData.rootFolder, '__temp', os.path.basename(file)), GlobalData.rootFolder)
            # 删除压缩文件
            for subFile, md5 in downloadList:
                delFile(os.path.join(GlobalData.rootFolder, '__temp', os.path.basename(subFile)))
        
    
    
class UpdateStatus(Enum):
    IGNORE = 0
    LASTEST = 1
    UPDATE = 2
    NOT_DEPLOY = 3
    LOAD_FAILURE = 4





















