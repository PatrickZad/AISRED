from support.lablesupport import LableGenerator
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

    def __init__(self, dataDispatcher, nlpExecutor):
        self.nlp = nlpExecutor
        self.lable = LableGenerator(self.nlp)
        self.dataTool = dataDispatcher

    '''
    param:
        gwtIdList:通过网页选择的gwt id的list
    return：
        无    
    '''

    def generateRUCMs(self, gwtIdList=None, gwtList=None):
        '''
        根据id获取要处理的GWT,返回的是未加标签的TaggedGWT
        为这一组GWT添加标签填充成TaggedGWT
        将这一组TaggedGWT合成一组RUCM
        '''
        if gwtList is None:
            self.GWTs = self.dataTool.get_gwt_list_by_id(gwtIdList)
        else:
            self.GWTs = gwtList
        taggedList = self.lable.generateLable(self.GWTs)
        # 根据useCaseName分组
        useCaseSet = list(set([taggedGWT.useCaseName for taggedGWT in taggedList]))
        useCaseDict = {}
        for name in useCaseSet:
            useCaseDict.setdefault(name, [])
        for taggedGWT in taggedList:
            useCaseDict[taggedGWT.useCaseName].append(taggedGWT)
        self.RUCMs = []
        for gwtList in useCaseDict.values():
            rucm = self.__generateRUCM(gwtList)
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
        # TODO 根据关键字从given和when的句子中取得Dependency，Generalization暂定为None,
        rucm.dependency = 'None'
        for taggedGWT in taggedList:
            if taggedGWT.flowType == 'basic':
                startGWT = taggedGWT  # 标记初始GWT
                rucm.precondition = startGWT.commonPrec
                rucm.primaryActor=startGWT.PrimaryActor
                rucm.secondaryActors=startGWT.SecondaryActors
                for sentence in taggedGWT.Givens:
                    '''
                    if sentence.stype == 'precondition':
                        rucm.precondition = rucm.precondition + sentence.content
                        '''
                    # TODO 根据关键字从given和when的action中取得Dependency，Generalization暂定为None,
                    self.__addDependency(rucm, sentence)
                # NTODO 命名实体识别获取Actor 暂定为获取各句第一个命名实体，取最多的为PrimaryActor，sencond暂定为None
                # entityList = []
                for sentence in taggedGWT.Whens:
                    if sentence.stype == 'action':
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
        self.__basicFlow(startGWT, rucm)
        self.__alternativeFlow(taggedList, rucm)
        return rucm

    '''
    param:
        taggedList:从数据库取得的待处理的TaggedGWT的list
        rucm:不完整的rucm对象等待填充
    return:
        修改对象，不返回新值
    '''

    def __briefDescription(self, taggedList, rucm):  # TODO 实现方法待改进
        scenario = ''
        rucm.briefDescription = ''
        for taggedGWT in taggedList:
            scenario = scenario + taggedGWT.Scenario
        brSentences = self.nlp.generateSummary(scenario)
        for br in brSentences:
            rucm.briefDescription = rucm.briefDescription + br['sentence']

    '''
    param:
        start:BasicFlow的首个gwt
        rucm:不完整的rucm对象等待填充
    return:
        修改对象，不返回新值
    '''

    def __basicFlow(self, start, rucm):
        rucm.basic = BasicFlow()
        rucm.basic.actions = [sentence.content for sentence in start.Whens if sentence.stype == 'action']
        # TODO 假定postScenario指向唯一的后继gwt
        while start.postScenarios is not None:
            for sentence in start.postScenarios.Whens:
                if sentence.stype == 'action':
                    rucm.basic.addAction(sentence.content)
            start = start.postScenarios
        for sentence in start.Thens:
            if sentence.stype == 'postcondition':
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
                specificAlt = SpecificFlow()
                rucm.basic.actions[taggedGWT.BranchScenarios[0]] = \
                    self.nlp.addValidate(rucm.basic.actions[taggedGWT.BranchScenarios[0]])
                specificAlt.rfs = taggedGWT.BranchScenarios[1]
                specificAlt.actions = [sentence.content for sentence in taggedGWT.Whens[taggedGWT.BranchScenarios[0]-1:]
                                            if sentence.stype == 'action']  # TODO 选择的action范围
                for sentence in taggedGWT.Thens:
                    if sentence.stype == 'postcondition':
                        specificAlt.postCondition += sentence.content
                rucm.specificAlt.append(specificAlt)
            elif taggedGWT.flowType == 'bounded':
                boundedAlt = BoundedFlow()
                boundedAlt.rfs = taggedGWT.BranchScenarios
                boundedAlt.actions = [sentence.content for sentence in taggedGWT.Whens[taggedGWT.BranchScenarios[0]-1:] if
                                           sentence.stype == 'action']  # TODO 选择的action范围
                for sentence in taggedGWT.Thens:
                    if sentence.stype == 'postcondition':
                        boundedAlt.postCondition += sentence.content
                rucm.boundedAlt.append(boundedAlt)
            elif taggedGWT.flowType == 'global':
                globalAlt = GlobalFlow()
                for i in range(0, len(taggedGWT.Givens) - 1):
                    if taggedGWT.Givens[i].stype == 'precondition':
                        contentGroup = re.match(r'.*GLOBAL.*', taggedGWT.Givens[i].content)
                        if contentGroup:
                            globalAlt.condition += taggedGWT.Givens[i+1].content
                globalAlt.actions = [sentence.content for sentence in taggedGWT.Whens if
                                          sentence.stype == 'action']
                for sentence in taggedGWT.Thens:
                    if sentence.stype == 'postcondition':
                        globalAlt.postCondition += sentence.content
                rucm.globalAlt.append(globalAlt)

    '''
    param:
        无
    return:
        无
    '''

    def __generateOutput(self):
        outpath = './' + str(datetime.now().timestamp()) + '.rucmout'
        self.output = ''
        for rucm in self.RUCMs:
            self.output += rucm.__str__()
        with open(outpath, 'w',encoding='utf-8') as f:
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


if __name__ == '__main__':
    from data.datatype import TaggedGWT, Sentence
    from support.nlpsupport import NLPExecutor
    import pickle

    file = r'../testfile/inputdemo.gwtfile'
    nlpTool = NLPExecutor(r'../stanford-corenlp-full-2018-10-05')
    '''
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
    gwtTextList = text.split('Story:')[1:]
    testList = []
    for gwtText in gwtTextList:
        gwtText = gwtText.replace('\n', '')
        contentGroup = re.match('\s*(.*)\s*Scenario:\s*(.*)\s*Business\sRule:\s*(.*)'
                                'Given:\s*Preconditions:\s*(.*)\s*Fixed\sdata:\s*(.*)'
                                'When:\s*Action:\s*(.*)\s*Input\sdata:\s*(.*)'
                                'Then:\s*Output\sdata:\s*(.*)\s*Postcondition:\s*(.*)\s*', gwtText)
        originGWT = TaggedGWT()
        originGWT.Features = []
        originGWT.Scenario = contentGroup.group(2)
        originGWT.Givens = []
        originGWT.Whens = []
        originGWT.Thens = []
        sentence = Sentence(stype='story', content=contentGroup.group(1))
        originGWT.Features.append(sentence)
        sentence = Sentence(stype='business_rule', content=contentGroup.group(3))
        originGWT.Features.append(sentence)
        sentList = nlpTool.splitSentences(contentGroup.group(4))
        for item in sentList:
            sentence = Sentence(stype='precondition', content=item)
            originGWT.Givens.append(sentence)
        sentence = Sentence(stype='fixed_data', content=contentGroup.group(5))
        originGWT.Givens.append(sentence)
        sentList = nlpTool.splitSentences(contentGroup.group(6))
        for i in range(0, len(sentList)):
            sentence = Sentence(stype='action', content=sentList[i], sequence=i + 1)
            originGWT.Whens.append(sentence)
        sentence = Sentence(stype='inputdata', content=contentGroup.group(7))
        originGWT.Whens.append(sentence)
        sentence = Sentence(stype='outputdata', content=contentGroup.group(8))
        originGWT.Thens.append(sentence)
        sentList = nlpTool.splitSentences(contentGroup.group(9))
        for item in sentList:
            sentence = Sentence(stype='postcondition', content=item)
            originGWT.Thens.append(sentence)
        testList.append(originGWT)
    '''
    with open('./testlist', 'rb') as f:
        testList = pickle.load(f)
    #    with open('./testlist', 'wb') as f:
    #       pickle.dump(testList, f)
    rucmResp = RUCMGnerator(None, nlpTool)
    rucmResp.generateRUCMs(gwtList=testList)
