#coding=utf-8
import json
import zlib

from _core.data import UserData
from _core.utils.httpUtil import httpGet


class VersionFile(UserData):
    '''版本文件类'''
    
    def resetByUrl(self, url):
        '''通过get请求获取版本文件'''
        content = httpGet(url)
        content = zlib.decompress(content)
        self._versionDict = json.loads(content.decode())
    
    def export(self, versionFile):
        '''输出版本文件'''
        content = json.dumps(self._versionDict, separators=(',', ':'), sort_keys=True)
        content = zlib.compress(content.encode(), 9)
        with open(versionFile, 'wb') as f:
            f.write(content)
    
    def getFileVersion(self, file):
        '''获取文件版本'''
        if file in self.data:
            return self.data[file]
        return None
    
    def setFileVersion(self, file, version):
        '''更新文件版本'''
        if not self.data:
            self.data = {} 
        self.data[file] = version
        self.flush()




# if __name__ == '__main__':
#     GlobalData.rootFolder = 'D:\\workspace\\eclipse\\ezjob\\__export__'
#     verFile = VersionFile('localVersion')
    # 测试写入
#     verFile.setFileVersion('abc.png', ['ddddd', 'eeeeee', 'ffffff'])
#     verFile.setFileVersion('def.png', ['dddddss', 'eeeeeess', 'ffffffss'])


    
    
    
    
    
    
    
    
    
    
    
    
    
    
