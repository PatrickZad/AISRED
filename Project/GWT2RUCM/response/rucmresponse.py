from support.lablesupport import LableGenerator
from support.nlpsupport import NLPExecutor
class RUCMGnerator():
    '''
    dataDispatcher:由上层传入DataDispatcher
    '''
    def __init__(self,dataDispatcher):
        self.nlp=NLPExecutor(r'../stanford-corenlp-full-2018-10-05',lang='zh')
        self.lable=LableGenerator(self.nlp)
        self.dataTool=dataDispatcher
    '''
    gwtIdList:通过网页选择的gwt id的list
    '''
    def generateRUCMs(self,gwtIdList):
        self.GWTs=dataTool.
        '''
        根据id获取要处理的GWT,返回的是未加标签的TaggedGWT
        为这一组GWT添加标签填充成TaggedGWT
        将这一组TaggedGWT合成一组RUCM
        '''
        pass
    '''
    gwtList:从数据库取得的待处理的TaggedGWT的list
    '''
    def __generateRUCM(self,gwtList):
        pass
    '''
    gwtList:从数据库取得的待处理的TaggedGWT的list
    rucm:不完整的rucm对象等待填充
    '''
    def __briefDescription(self,gwtList,rucm):
        pass
    '''
    gwtList:从数据库取得的待处理的TaggedGWT的list
    rucm:不完整的rucm对象等待填充
    '''
    def __basicFlow(self,gwtList,rucm):
        pass
    '''
    gwtList:从数据库取得的待处理的TaggedGWT的list
    rucm:不完整的rucm对象等待填充
    '''
    def __alternativeFlow(self,gwtList,rucm):
        pass
    '''
    rucmList:转换完整的rucm对象的list
    '''
    def __generateOutput(self,rucmList):
        pass
    