from support.lablesupport import LableGenerator
from support.nlpsupport import NLPExecutor
from data.datatype import RUCM, BasicFlow, SpecificFlow, BoundedFlow, GlobalFlow
from datetime import datetime
import re


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
        self.__briefDescription(self.startGWT, rucm)
        rucm.precondition = self.startGWT.commonPrec
        # TODO 根据关键字从given和when的句子中取得Dependency，Generalization暂定为None,
        rucm.dependency = ''
        for taggedGWT in taggedList:
            if taggedGWT.flowType == 'basic':
                self.startGWT = taggedGWT  # 标记初始GWT
                for sentence in taggedGWT.Givens:
                    '''
                    if sentence.type == 'precondition':
                        rucm.precondition = rucm.precondition + sentence.content
                        '''
                    # TODO 根据关键字从given和when的action中取得Dependency，Generalization暂定为None,
                    self.__addDependency(rucm, sentence)
                # NTODO 命名实体识别获取Actor 暂定为获取各句第一个命名实体，取最多的为PrimaryActor，sencond暂定为None
                # entityList = []
                for sentence in taggedGWT.Whens:
                    if sentence.type == 'action':
                        # TODO 根据关键字从given和when的action中取得Dependency，Generalization暂定为None,
                        self.__addDependency(rucm, sentence)
                        '''
                        entityList.append(self.nlp.firstNamedEntities(sentence))
                        entityDict = {}
                        for entity in entityList:
                            if entity in entityDict:
                                entityDict[entity] = entityDict[entity] + 1
                            else:
                                entityDict[entity] = 1
                        actor = 'None'
                        num = 0
                        for entity, amount in entityDict.items():
                            if amount > num and entity != '系统 ':
                                actor = entity
                        rucm.primaryActor = actor
                        rucm.secondaryActors = 'None'
                        '''
        # TODO 根据关键字从given和when的action中取得Dependency，Generalization暂定为None,
        rucm.generalization = 'None'
        self.__basicFlow(self.startGWT, rucm)
        self.__alternativeFlow(taggedList, rucm)
        return rucm

    '''
    param:
        taggedList:从数据库取得的待处理的TaggedGWT的list
        rucm:不完整的rucm对象等待填充
    return:
        修改对象，不返回新值
    '''

    def __briefDescription(self, taggedList, rucm):
        scenario = ''
        for taggedGWT in taggedList:
            scenario = scenario + taggedGWT.Scenario
        brSentences = self.nlp.generateSummary(scenario)
        for sentence in brSentences:
            rucm.briefDescription = rucm.briefDescription + sentence

    '''
    param:
        start:BasicFlow的首个gwt
        rucm:不完整的rucm对象等待填充
    return:
        修改对象，不返回新值
    '''

    def __basicFlow(self, start, rucm):
        rucm.basic = BasicFlow()
        rucm.basic.actions = [sentence.content for sentence in start.Whens if sentence.type == 'action']
        # TODO 假定postScenario指向唯一的后继gwt
        while start.postScenarios is not None:
            for sentence in start.postScenarios.Whens:
                if sentence.type == 'action':
                    rucm.basic.addAction(sentence.content)
            start = start.postScenarios
        for sentence in start.Thens:
            if sentence.type == 'postcondition':
                rucm.basic.postCondition += sentence.content

    '''
    param:
        taggedList:从数据库取得的待处理的TaggedGWT的list
        rucm:不完整的rucm对象等待填充
    return:
        修改对象，不返回新值
    '''

    def __alternativeFlow(self, taggedList, rucm):
        # TODO 如何生成
        rucm.specificAlt = []
        rucm.boundedAlt = []
        rucm.globalAlt = []
        for taggedGWT in taggedList:
            if taggedGWT.flowType == 'specific':
                rucm.specificAlt = SpecificFlow()
                rucm.basic.actions[taggedGWT.BranchScenarios[0]] = \
                    self.nlp.addValidate(rucm.basic.actions[taggedGWT.BranchScenarios[0]])
                rucm.specificAlt.rfs = taggedGWT.BranchScenarios[1]
                rucm.specificAlt.actions = [sentence.content for sentence in taggedGWT.Whens
                                            if sentence.type == 'action']
                for sentence in taggedGWT.Thens:
                    if sentence.type == 'postcondition':
                        rucm.specificAlt.postCondition += sentence.content
            elif taggedGWT.flowType == 'bounded':
                rucm.boundedAlt = BoundedFlow()
                rucm.boundedAlt.rfs = taggedGWT.BranchScenarios
                rucm.boundedAlt.actions = [sentence.content for sentence in taggedGWT.Whens if
                                           sentence.type == 'action']
                for sentence in taggedGWT.Thens:
                    if sentence.type == 'postcondition':
                        rucm.boundedAlt.postCondition += sentence.content
            elif taggedGWT.flowType == 'global':
                rucm.globalAlt = GlobalFlow()
                for sentence in taggedGWT.Givens:
                    if sentence.type == 'precondition':
                        contentGroup = re.match(r'.*GLOBAL\s*([\u4e00-\u9fa5]+)', sentence.content)
                        if contentGroup:
                            rucm.globalAlt.condition += contentGroup.group(1)
                rucm.globalAlt.actions = [sentence.content for sentence in taggedGWT.Whens if
                                          sentence.type == 'action']
                for sentence in taggedGWT.Thens:
                    if sentence.type == 'postcondition':
                        rucm.globalAlt.postCondition += sentence.content

    '''
    param:
        无
    return:
        无
    '''

    def __generateOutput(self):
        outpath = r'../outputfile/' + str(datetime.now().timestamp()) + r'.rucmout'
        self.output = ''
        for rucm in self.RUCMs:
            self.output += rucm.__str__()
        with open(outpath, 'w') as f:
            f.write(self.output)
        self.output = outpath

    def __addDependency(self, rucm, sentence):
        # TODO 根据关键字从given和when的action中取得Dependency，Generalization暂定为None,
        inclu = re.match(r'INCLUDE\s*([\u4e00-\u9fa5]+).+', sentence.content)
        if inclu:
            rucm.dependency += 'INCLUDE USE CASE' + inclu.group(1) + ' '
        extd = re.match(r'EXTENDED\s*([\u4e00-\u9fa5]+).+', sentence.content)
        if extd:
            rucm.dependency += 'EXTENDED BY USE CASE ' + extd.group(1) + ' '
