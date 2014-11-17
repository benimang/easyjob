#coding=utf-8

'''
Created on 2014年7月17日
@author: Beni
'''

from builtins import getattr
import ctypes


STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE= -11
STD_ERROR_HANDLE = -12
 
FOREGROUND_BLACK = 0x0
FOREGROUND_BLUE = 0x01      # text color contains blue.
FOREGROUND_GREEN= 0x02      # text color contains green.
FOREGROUND_RED = 0x04       # text color contains red.
FOREGROUND_INTENSITY = 0x08 # text color is intensified.

WHITE  = FOREGROUND_RED   | FOREGROUND_GREEN     | FOREGROUND_BLUE      | FOREGROUND_INTENSITY
RED    = FOREGROUND_RED   | FOREGROUND_INTENSITY
GREEN  = FOREGROUND_GREEN | FOREGROUND_INTENSITY
BLUE   = FOREGROUND_BLUE  | FOREGROUND_INTENSITY
YELLOW = FOREGROUND_RED   | FOREGROUND_GREEN     | FOREGROUND_INTENSITY
PURPLE = FOREGROUND_RED   | FOREGROUND_BLUE      | FOREGROUND_INTENSITY
SKY    = FOREGROUND_GREEN | FOREGROUND_BLUE      | FOREGROUND_INTENSITY

_currentColor = WHITE
_indent = 0

def _changeColor(color):
    global _currentColor
    if _currentColor != color:
        _currentColor = color
        std_out_handle = getattr(ctypes.windll.kernel32, 'GetStdHandle')(STD_OUTPUT_HANDLE)
        getattr(ctypes.windll.kernel32, 'SetConsoleTextAttribute')(std_out_handle, color)

def getTraceIndent(value):
    return _indent

def setTraceIndent(value):
    _indent = value

def addTraceIndent(value):
    global _indent
    _indent = max(0, _indent + value)


def trace(msg='', *parList, **parKey):
    _changeColor(WHITE)
    msg = _indent * '    ' + str(msg)
    print(msg, *parList, **parKey)

def traceRed(msg='', *parList, **parKey):
    _changeColor(RED)
    msg = _indent * '    ' + str(msg)
    print(msg, *parList, **parKey)
    
def traceGreen(msg='', *parList, **parKey):
    _changeColor(GREEN)
    msg = _indent * '    ' + str(msg)
    print(msg, *parList, **parKey)
    
def traceBlue(msg='', *parList, **parKey):
    _changeColor(BLUE)
    msg = _indent * '    ' + str(msg)
    print(msg, *parList, **parKey)
    
def traceYellow(msg='', *parList, **parKey):
    _changeColor(YELLOW)
    msg = _indent * '    ' + str(msg)
    print(msg, *parList, **parKey)
    
def tracePurple(msg='', *parList, **parKey):
    _changeColor(PURPLE)
    msg = _indent * '    ' + str(msg)
    print(msg, *parList, **parKey)
    
def traceSky(msg='', *parList, **parKey):
    _changeColor(SKY)
    msg = _indent * '    ' + str(msg)
    print(msg, *parList, **parKey)
    
    
    
    