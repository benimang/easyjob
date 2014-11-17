#coding=utf-8
import os
import pickle


class GlobalData():
    '''全局数据'''
    rootFolder = '' # 程序根目录


class UserData():
    '''用户数据（本地持久化对象）'''
    
    def __init__(self, key):
        self._key = key
        self.refresh()
        
    def getKey(self):
        return self._key
    
    def getFile(self):
        return os.path.join(GlobalData.rootFolder, '__userdata', self._key + '.data')
        
    def refresh(self):
        try:
            with open( self.getFile() , 'rb') as f:
                self.data = pickle.load(f)
        except:
            self.data = None
        
    def flush(self):
        with open(self.getFile(), 'wb') as f:
            pickle.dump(self.data, f)
            





# if __name__ == '__main__':
#     GlobalData.rootFolder = 'D:\\workspace\\eclipse\\ezjob\\__export__'
#     xx = UserData('testUD')
#     xx.data = ['中文', 123, 'abcd']
#     xx.flush()
#     xx.refresh()
#     print(xx.data)