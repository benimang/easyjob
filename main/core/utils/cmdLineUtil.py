#coding=utf-8
'''
Created on 2013-5-21
@author: Beni
'''

import subprocess

from core.utils.traceUtil import trace


def executeCmdLine(cmdLine, isTraceCmdLine=True, isTraceDetail=True, encoding='gbk'):
    '''调动命令行'''
    result = []
    if isTraceCmdLine:
        trace(cmdLine)
    p = subprocess.Popen(cmdLine, stdout=subprocess.PIPE, shell=True)
    for line in p.stdout:
        result.append(line)
        if isTraceDetail:
            trace(line.decode(encoding).strip())
    executeStatus = p.wait()
    p.kill()
    if executeStatus != 0:
        raise Exception('执行命令行异常')
    return result