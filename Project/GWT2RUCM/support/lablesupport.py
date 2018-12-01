class LableGenerator():
    '''
    nlpExecutor:nlp工具类实例，由上层传入
    '''
    def __init__(self, nlpExecutor):
        self.nlp = nlpExecutor
    '''
    param：
        gwtList:未标签化的gwt的list，每个元素的类型为TaggedGWT
    return：
        修改对象，不返回新值
    '''
    def generateLable(self,gwtList):
        pass

    def __simpleLable(self):
        pass

    def __normalize(self):
        pass

    def __addGWTLable(self):
        pass
