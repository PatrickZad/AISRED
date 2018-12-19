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

    def __init__(self, nlpExecutor):
        self.nlp = nlpExecutor
        self.lable = LableGenerator(self.nlp)

    '''
    param:
        gwtList:原始GWT集合
    return：
        无    
    '''

    def generateRUCMs(self, gwtList):
        # 根据Feature分组
        featureSet = list(set([gwt.Feature for gwt in gwtList]))
        featureDict = {}
        for feature in featureSet:
            featureDict.setdefault(feature, [])
        for gwt in gwtList:
            featureDict[gwt.feature].append(gwt)
        self.RUCMs = []
        for gwtList in featureDict.values():
            rucm = self.__generateRUCM(gwtList)
            self.RUCMs.append(rucm)
        self.__generateOutput()

    '''
    param:
        gwtList:待处理的GWT的list
    return：
        rucm:由输入合成的rucm实例
    '''

    def __generateRUCM(self, gwtList):
        taggedList = self.lable.generateLable(gwtList)
        rucm = RUCM(taggedList[0].useCaseName)
        self.__briefDescription(taggedList, rucm)
        # TODO 根据关键字从given和when的句子中取得Dependency，Generalization暂定为None,
        rucm.primaryActor, rucm.secondaryActors = self.__actors(taggedList, rucm)
        rucm.dependency = 'None'
        '''
        for taggedGWT in taggedList:
            if taggedGWT.flowType == 'basic':
                startGWT = taggedGWT  # 标记初始GWT
                rucm.precondition = startGWT.Givens
                
                for sentence in taggedGWT.Givens:
                    
                    if sentence.stype == 'precondition':
                        rucm.precondition = rucm.precondition + sentence.content
                        
                    # TODO 根据关键字从given和when的action中取得Dependency，Generalization暂定为None,
                    self.__addDependency(rucm, sentence)
                # NTODO 命名实体识别获取Actor 暂定为获取各句第一个命名实体，取最多的为PrimaryActor，sencond暂定为None
                # entityList = []
                for sentence in taggedGWT.Whens:
                    if sentence.stype == 'action':
                        # TODO 根据关键字从given和when的action中取得Dependency，Generalization暂定为None,
                        self.__addDependency(rucm, sentence)
                        '''
        # TODO 根据关键字从given和when的action中取得Dependency，Generalization暂定为None,
        rucm.generalization = 'None'
        self.__basicFlow(taggedList, rucm)
        self.__alternativeFlow(taggedList, rucm)
        return rucm

    '''
    param:
        taggedList:待处理的TaggedGWT的list
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
        taggedList:待处理的TaggedGWT的list
        rucm:不完整的rucm对象等待填充
    return:
        修改对象，不返回新值
    '''

    def __actors(self, taggedList, rucm):
        actorlist = []
        for gwt in taggedList:
            actorlist = actorlist + [sent.actor for sent in gwt.Whens]
        actorSet = list(set(actorlist))
        actorDict = {}
        for actor in actorSet:
            actorDict.setdefault(actor, 0)
        for actor in actorlist:
            actorDict[actor] += 1
        actorSet.remove('系统')  # TODO 去除表示此系统的actor方法待改进
        actorDict.pop('系统')
        primary = actorSet[0]
        for actor in actorDict.keys():
            if actorDict[actor] > actorDict[primary]:
                primary = actor
        actorSet.remove(primary)
        return primary, actorSet

    '''
    param:
        start:BasicFlow的首个gwt
        rucm:不完整的rucm对象等待填充
    return:
        修改对象，不返回新值
    '''

    def __basicFlow(self, taggelist, rucm):
        rucm.basic = BasicFlow()
        for gwt in taggelist:
            if gwt.flowType == 'basic':
                start = gwt
        rucm.basic.actions = [sentence.normalContent for sentence in start.Whens]
        for sentence in start.Thens:
            rucm.basic.postCondition += sentence.normalContent

    '''
    param:
        taggedList:待处理的TaggedGWT的list
        rucm:不完整的rucm对象等待填充
    return:
        修改对象，不返回新值
    '''

    def __alternativeFlow(self, taggedList, rucm):
        rucm.specificAlt = []
        rucm.boundedAlt = []
        rucm.globalAlt = []
        for taggedGWT in taggedList:
            if taggedGWT.flowType == 'specific':
                specificAlt = SpecificFlow()
                action=rucm.basic.Whens[taggedGWT.refer].action
                action=rucm.basic.Whens[taggedGWT.refer].wordlist[action]
                rucm.basic.Whens[taggedGWT.refer].normalContemt.replace(action,'VALIDATES THAT')
                specificAlt.rfs = taggedGWT.refer+1#TODO 考虑记录一个偏移量来包括条件action和循环action拆分占据的序号
                specificAlt.actions = [sentence.normalContent for sentence in
                                       taggedGWT.Whens[taggedGWT.refer+1:]]
                for sentence in taggedGWT.Thens:
                    specificAlt.postCondition += sentence.normalContent
                rucm.specificAlt.append(specificAlt)
            elif taggedGWT.flowType == 'bounded':
                boundedAlt = BoundedFlow()
                boundedAlt.rfs = [num+1 for num in taggedGWT.refer]
                boundedAlt.actions = [sentence.normalContent for sentence in
                                      taggedGWT.Whens[taggedGWT.refer[0]+1:]]  # TODO 选择的action范围
                for sentence in taggedGWT.Thens:
                    boundedAlt.postCondition += sentence.content
                rucm.boundedAlt.append(boundedAlt)
            elif taggedGWT.flowType == 'global':
                globalAlt = GlobalFlow()
                globalAlt.condition = taggedGWT.condition.originContent
                globalAlt.actions = [sentence.normalContent for sentence in taggedGWT.Whens ]
                for sentence in taggedGWT.Thens:
                    globalAlt.postCondition += sentence.normalContent
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
        with open(outpath, 'w', encoding='utf-8') as f:
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
    # from data.datatype import TaggedGWT, Sentence
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
    with open('./testlist', 'wb') as f:
         pickle.dump(testList, f)
    '''
    with open('./testlist', 'rb') as f:
        testList = pickle.load(f)

    rucmResp = RUCMGnerator(None, nlpTool)
    rucmResp.generateRUCMs(gwtList=testList)
