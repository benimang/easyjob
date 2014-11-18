#coding=utf-8
'''
Created on 2013-1-10
@author: Beni
'''

from genericpath import getsize
import hashlib
import os
import shutil

from _core.utils.traceUtil import trace


def mkDirs(path):
    '''创建文件夹'''
    if os.path.isdir(path):
        return
    ary = path.split(os.sep)
    currentPath = ary.pop(0)
    for item in ary:
        currentPath = os.sep.join((currentPath, item))
        if not os.path.isdir(currentPath):
            trace('创建目录 ' + currentPath)
            os.mkdir(currentPath)
            
            
def delFile(file):
    '''删除文件或文件夹'''
    if os.path.isdir(file):
        trace('删除目录 ' + file)
        shutil.rmtree(file)
    elif os.path.isfile(file):
        trace('删除文件 ' + file)
        os.remove(file)
    
    
def renameFile(file, newName):
    '''重命名文件或文件夹'''
    newFile = os.sep.join((os.path.dirname(file), newName))
    os.rename(file, newFile)
    return newFile
    
    
def copyFile(srcFile, dstFile):
    '''复制文件或文件夹'''
    if not os.path.exists(srcFile):
        raise Exception('无法执行copyFile操作，指定文件或路径不存在（{0}）'.format(srcFile))
    if os.path.isdir(srcFile):
        #mkDirs(dstFile)
        shutil.copytree(srcFile, dstFile)
    else:
        #mkDirs(os.path.dirname(dstFile))
        shutil.copy(srcFile, dstFile)


def cutFile(file, size, isDelFile=True, outputFolder=None):
    '''根据尺寸切文件'''
    result = []
    num = 1
    fileName = os.path.basename(file)
    fileSize = getsize(file)
    if outputFolder == None:
        outputFolder = os.path.dirname(file)
    if fileSize <= size:
        targetFile = os.sep.join((outputFolder, fileName))
        if targetFile != file:
            copyFile(file, targetFile)
        result.append(targetFile)
        trace('无需生成碎片文件 ' + targetFile)
    else:
        with open(file, 'rb') as f:
            while True:
                content = f.read(size)
                if len(content) == 0:
                    break
                targetFile = os.sep.join((outputFolder, fileName+'.'+'%03d'%num))
                trace('生成碎片文件 ' + targetFile)
                with open(targetFile, 'wb') as subFile:
                    subFile.write(content)
                result.append(targetFile)
                num += 1
        if isDelFile:
            delFile(file)
    return tuple(sorted(result))


def moveFile(srcFile, dstFile):
    '''移动文件或文件夹'''
    copyFile(srcFile, dstFile)
    delFile(srcFile)
    

def getFileList(folder, ignoreList=[]):
    '''获取指定文件夹中文件列表（完整路径）'''
    fileList = os.listdir(folder)
    result = []
    for name in fileList:
        if name in ignoreList:
            continue
        result.append(os.sep.join((folder, name)))
    return result


def getAllFiles(folder, ignoreList=[]):
    '''获取文件夹中的所有文件（完整路径）'''
    fileList = getFileList(folder, ignoreList)
    result = []
    for file in fileList:
        if os.path.isdir(file):
            result.extend(getAllFiles(file, ignoreList))
        elif os.path.isfile(file):
            result.append(file)
    return result

def getAllFolders(folder, ignoreList=[]):
    '''获取文件中的所有文件夹（完整路径）'''
    fileList = getFileList(folder, ignoreList)
    result = []
    for file in fileList:
        if os.path.isdir(file):
            result.append(file)
            result.extend(getAllFolders(file, ignoreList))
    return result
    

def clearFolder(folder):
    '''清空目录'''
    delFile(folder)
    mkDirs(folder)
    
    
def getFileMd5(file):
    '''获取文件的md5'''
    with open(file, 'rb') as f:
        result = hashlib.md5(f.read()).hexdigest()
    trace('计算文件MD5 ' + file + ' => ' + result)
    return result


def getFileExtName(file):
    '''获取文件的扩展名（返回强制小写）'''
    return file[file.rfind('.')+1:].lower()