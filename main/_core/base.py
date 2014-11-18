#coding=utf-8

def getSingleton(clazz):
    '''
    获取单例
    @param clazz: 需要创建或获取单例的类
    @return: 类的单例
    '''
    
    if not hasattr(clazz, '__instance__'):
        clazz.__instance__ = clazz()
    return clazz.__instance__












