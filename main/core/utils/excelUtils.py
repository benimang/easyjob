#coding=utf-8
'''
Created on 2013-1-11
@author: Beni
'''


class ConfigSheet():
    '''配置文件excel表'''
    def __init__(self, sheet):
        '''构造函数'''
        self._sheet = sheet
        self._headers = self._sheet.row_values(1)
        for headerName in self._headers:
            if headerName == '':
                raise Exception('不允许出现空白字段名')
            if self._headers.count(headerName) > 1:
                raise Exception('不允许重复字段名（{0}）'.format(headerName))
        self._startRow = 6
        self._endRow = self._sheet.nrows
        self._range = range(self._startRow, self._endRow+1)
    
    def getCell(self, header, row):
        '''获取指定数据'''
        col = self._headers.index(header)
        return self._sheet.row_values(row-1)[col]
    
    def getCellAsInt(self, header, row):
        '''获取指定数据返回整形'''
        return int(self.getCell(header, row))
    
    def getCellAsStrInt(self, header, row):
        '''获取指定数据返回字符串形式的整形'''
        return str(self.getCellAsInt(header, row))
    
    def getStartRow(self):
        '''获取开始行数'''
        return self._startRow
    
    def getEndRow(self):
        '''获取结束行数'''
        return self._endRow
    
    def getRange(self):
        '''获取行数范围'''
        return self._range
        

if __name__ == '__main__':
    import xlrd3
    configFile = 'E:\\手游文档\\配置表-录入\\技能填表.xls'
    excel = xlrd3.open_workbook(configFile)
    sheet = excel.sheet_by_name('天赋')
    configSheet = ConfigSheet(sheet)
    for i in configSheet.getRange():
        print (i, configSheet.getCell('name', i))
    