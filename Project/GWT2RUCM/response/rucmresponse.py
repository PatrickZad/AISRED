from support.lablesupport import LableGenerator
from support.nlpsupport import NLPExecutor
from support.datasupport import GWTdao
from data.datatype import RUCM
from textrank4zh import TextRank4Sentence

class RUCMGnerator():
    '''
    param：
        dataDispatcher:由上层传入DataDispatche
    return：
        无
    '''

    def __init__(self, dataDispatcher):
        self.nlp = NLPExecutor(r'../stanford-corenlp-full-2018-10-05', lang='zh')
        self.lable = LableGenerator(self.nlp)
        self.dataTool = dataDispatcher

    '''
    param:
        gwtIdList:通过网页选择的gwt id的list
    return：
        无    
    '''

    def generateRUCMs(self, gwtIdList):
        '''
        根据id获取要处理的GWT,返回的是未加标签的TaggedGWT
        为这一组GWT添加标签填充成TaggedGWT
        将这一组TaggedGWT合成一组RUCM
        '''
        self.GWTs = self.dataTool.get_gwt_list_by_id(gwtIdList)
        taggedList = self.lable.generateLable(self.GWTs)
        # 根据useCaseName分组
        useCaseSet = list(set([taggedGWT.useCaseName for taggedGWT in taggedList]))
        useCaseList = []
        for i in range(0, len(useCaseSet)):
            useCaseList = useCaseList.append([])
        for taggedGWT in taggedList:
            useCaseList[useCaseSet.index(taggedGWT.useCaseName)].append(taggedGWT)
        self.RUCMs = []
        for i in range(0, len(useCaseList)):
            rucm = self.__generateRUCM(useCaseList[i])
            self.RUCMs.append(rucm)
        self.__generateOutput()

    '''
    param:
        taggedList:从数据库取得的待处理的TaggedGWT的list
    return：
        rucm:由输入合成的rucm实例
    '''

    def __generateRUCM(self, taggedList):
        rucm = RUCM(taggedList[0].useCaseName)
        self.__briefDescription(taggedList, rucm)
        rucm.precondition = ''
        for taggedGWT in taggedList:
            if taggedGWT.preScenarios == None:
                for sentence in taggedGWT.Givens:
                    if sentence.type == 'precondition':
                        rucm.precondition = rucm.precondition + sentence.content
        #TODO 命名实体识别获取Actor
        #TODO 根据关键字取得Dependency，Generalization
        self.__basicFlow(taggedList,rucm)
        self.__alternativeFlow(taggedList,rucm)

    '''
    param:
        taggedList:从数据库取得的待处理的TaggedGWT的list
        rucm:不完整的rucm对象等待填充
    return:
        修改对象，不返回新值
    '''

    def __briefDescription(self, taggedList, rucm):
        scenario=''
        for taggedGWT in taggedList:
            scenario=scenario+taggedGWT.Scenario
        tr=TextRank4Sentence()
        tr.analyze(text=scenario)
        rucm.briefDescription=''
        for sentence in tr.get_key_sentences(num=3):#TODO 摘要生成实现方法待选
            rucm.briefDescription=rucm.briefDescription+sentence

    '''
    param:
        taggedList:从数据库取得的待处理的TaggedGWT的list
        rucm:不完整的rucm对象等待填充
    return:
        修改对象，不返回新值
    '''

    def __basicFlow(self, taggedList, rucm):
        pass

    '''
    param:
        taggedList:从数据库取得的待处理的TaggedGWT的list
        rucm:不完整的rucm对象等待填充
    return:
        修改对象，不返回新值
    '''

    def __alternativeFlow(self, taggedList, rucm):
        pass

    '''
    param:
        无
    return:
        无
    '''

    def __generateOutput(self):
        pass
