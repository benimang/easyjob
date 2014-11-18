#coding=utf-8

'''
Created on 2014年7月18日
@author: Beni
'''
import os

from _core.data import GlobalData
from _core.utils.cmdLineUtil import executeCmdLine
from _core.utils.fileUtils import delFile, getFileMd5, mkDirs, cutFile, \
    getAllFiles, getAllFolders
from _core.utils.traceUtil import trace, addTraceIndent


def compress(outputFile, targetFile, volumeSize=2000000):
    '''
    创建压缩文件
    @param outputFile: 生成压缩文件
    @param targetFile: 压缩对象，可以是文件或文件夹
    @param volumeSize: 分卷尺寸，单位是字节，-1表示不使用分卷
    @return: 返回两个数组，一个是压缩文件的列表，一个是对应文件的MD5
    '''
    trace('创建压缩文件 ' + outputFile)
    
    md5s = []
    
    addTraceIndent(1)
    
    # 将所有文件设置时间
    if os.path.isfile(targetFile):
        os.utime(targetFile, (1383333333, 1383333333))
    else:
        for file in getAllFiles(targetFile):
            os.utime(file, (1383333333, 1383333333))
        for folder in getAllFolders(targetFile):
            print(folder)
            os.utime(folder, (1383333333, 1383333333))
    
    # 删除输出文件开头的所有文件
    zipfileFolder = os.path.dirname(outputFile)
    zipfileName = os.path.basename(outputFile)
    for file in os.listdir(zipfileFolder):
        if file.find(zipfileName + '.') == 0 or zipfileName == file:
            delFile(os.path.join(zipfileFolder, file))
    
    # 执行命令行压缩
    cmdLine = '{0} a {1} {2} '.format(_get7zCmd(), outputFile, targetFile)
    executeCmdLine( cmdLine )

    # 切割文件
    if volumeSize > -1:
        files = cutFile(outputFile, volumeSize)
        
    # 计算每个文件的md5
    for file in files:
        md5s.append( getFileMd5(os.path.join(zipfileFolder, file)) )
    
    addTraceIndent(-1)
    
    return files, md5s



def decompress(file, outputFolder):
    '''
    解压缩文件
    @param file: 解压缩文件
    @param outputFolder: 解压缩输出路径
    '''
    trace('解压缩文件 ' + file)
    
    addTraceIndent(1)
    
    if not os.path.isfile(file):
        file += '.001'
    
    # 创建输出目录
    mkDirs(os.path.dirname(outputFolder))
    
    # 执行命令行解压缩
    cmdLine = '{0} x {1} -o{2} -aoa'.format( _get7zCmd(), file, outputFolder )
    executeCmdLine( cmdLine )
    
    
    addTraceIndent(-1)



_7zCmd = None
def _get7zCmd():
    global _7zCmd
    if not _7zCmd:
        _7zCmd = os.path.join(GlobalData.rootFolder, '__software', '7z', '7z.exe')
    return _7zCmd



# rootFolder = 'D:\\workspace\\eclipse\\ezjob\\__export__'
# compress('C:\\Users\\Beni\\Desktop\\xx.7z', 'C:\\Users\\Beni\\Desktop\\easyjob')
# decompress('C:\\Users\\Beni\\Desktop\\xx.7z', 'C:\\Users\\Beni\\Desktop')


