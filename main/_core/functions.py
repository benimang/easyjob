#coding=utf-8

def getSingleton(clazz):
    '''
    获取单例
    @param clazz: 需要创建或获取单例的类
    @return: 类的单例
    '''
    global __instanceMap__
    if __instanceMap__ == None:
        __instanceMap__ = {}
    if clazz not in __instanceMap__:
        __instanceMap__[clazz] = clazz()
    return __instanceMap__[clazz]


def destroySingleton(clazz):
    '''
    销毁单例
    @param clazz: 需要销毁单例的类
    @return: None
    '''
    global __instanceMap__
    if __instanceMap__ and clazz in __instanceMap__:
        instance = __instanceMap__[clazz]
        if instance:
            del instance
        del __instanceMap__[clazz]
        










