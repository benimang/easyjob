#coding=utf-8
'''
Created on 2013-1-19
@author: Beni
'''

import sys, os


def getCmdInfoByStr(par, cmdName):
    '''根据命名头部文本信息获取命令信息'''
    if not isinstance(par, list):
        msgAry = par.split('\n')
    else:
        msgAry = par
    result = {}
    nameAry = []
    versionAry = []
    parAry = []
    descAry = []
    aryMap = {
              '#name#': nameAry,
              '#version#': versionAry,
              '#desc#': descAry,
              '#par#': parAry,
              }
    targetAry = None
    for line in msgAry:
        if line == '':
            continue
        if line in aryMap:
            targetAry = aryMap[line]
            continue
        if targetAry != None:
            targetAry.append(line)
    result['name'] = cmdName
    result['exeName'] = ' '.join(nameAry)
    result['desc'] = '\n'.join(descAry)
    result['version'] = ''.join(versionAry)
    parListAry = []
    result['parList'] = parListAry
    for line in parAry:
        subAry = line.split(' ')
        if len(subAry) < 3:
            raise Exception('命令头文件中参数格式不正确，少于3项（{0}）'.format(line))
        item = {}
        item['parName'] = subAry[0]
        item['par'] = subAry[1]
        item['batValue'] = subAry[2]
        item['shValue'] = subAry[3 if len(subAry) > 3 else 2]
        parListAry.append(item)
    return result
    


def getCmdInfo(file):
    '''获取指定命令文件的命令信息'''
    msgAry = []
    s = '\'\'\''
    with open(file, 'r', encoding='utf_8') as f:
        isStart = False
        for line in f:
            if line.count(s) > 1:
                raise Exception('命令文件头部格式不正确（{0}）'.format(file))
            isTargetLine = s in line
            if isStart:
                if isTargetLine:
                    msgAry.append(line[:line.find(s)].strip())
                    break
                else:
                    msgAry.append(line.strip())
            elif isTargetLine:
                msgAry.append(line[line.find(s)+len(s):].strip())
                isStart = True
        else:
            raise Exception('命令文件没有包含合法头部结构（{0}）'.format(file))
    fileBaseName = os.path.basename(file)
    return getCmdInfoByStr(msgAry, fileBaseName[:fileBaseName.rfind('.')])


def echoInfo(msg, tabNum=0):
    '''输出命令里的日志信息'''
    print ('{0}--> {1}'.format(tabNum*'    ', msg))


def echoFun(fun, tabNum=0, msg=''):
    '''输出命令的函数信息'''
    if tabNum > 0:
        echoInfo(fun.__doc__ + msg, tabNum)
    else:
        print(fun.__doc__)
    

def initDebugPar():
    '''初始化调试参数，用于单个命令文件独立本地测试'''
    file = sys.argv.pop(0)
    info = getCmdInfo(file)
    for par in info['parList']:
        sys.argv.append(par['batValue'])


def testCmd(batFile=''):
    '''在开发环境下测试命令'''
    file = sys.argv.pop(0)
    sys.argv = []
    info = getCmdInfo(file)
    for par in info['parList']:
        sys.argv.append(par['batValue'])
    # 插入测试命令的中文名称
    sys.argv.insert(0, info['version'])
    # 插入测试命令的版本
    sys.argv.insert(0, info['name'])
    # 插入空白代替下载URL
    sys.argv.insert(0, '')
    # 插入bat文件全路径以及文件名
    if batFile == '':
        batFullName = ''
        batPath = ''
    else:
        batFullName = batFile
        batPath = batFile[:batFile.rfind(os.sep)]
    sys.argv.insert(0, batFullName)
    sys.argv.insert(0, batPath)
    # 插入pyTool工作路径
    import __cmd__.buildPyTool
    sys.argv.insert(0, __cmd__.buildPyTool.WORK_PATH)
    # 插入空白代替入口第一个参数
    sys.argv.insert(0, '')
    
    # 开始执行逻辑
    import pyTool
    pyTool.main()
    

if __name__ == '__main__':
    path = '../cmd/buildPyTool.py'
    initDebugPar()