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
            featureDict[gwt.Feature].append(gwt)
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
        rucm.precondition=''
        for sent in self.start.Givens:
            rucm.precondition+=sent.originContent
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
            scenario = scenario + taggedGWT.scenarioStr()
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
            actorlist = actorlist + [sent.wordlist[sent.actor] for sent in gwt.Whens if sent.actor is not None]
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
        actorSet.remove(primary)#TODO secondary actor的生成待改进
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
               self.start = gwt
               break
        rucm.basic.actions = [sentence.normalContent for sentence in self.start.Whens]
        for sentence in self.start.Thens:
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
                action = self.start.Whens[taggedGWT.refer].action
                action = self.start.Whens[taggedGWT.refer].wordlist[action] 
                sent=rucm.basic.actions[taggedGWT.refer]
                sent=sent.replace(action, 'VALIDATES THAT')
                #sent='系统 VALIDATES THAT '+sent
                rucm.basic.actions[taggedGWT.refer]=sent
                specificAlt.rfs = taggedGWT.refer + 1  # TODO 考虑记录一个偏移量来包括条件action和循环action拆分占据的序号
                specificAlt.actions = [sentence.normalContent for sentence in
                                       taggedGWT.Whens] 
                for sentence in taggedGWT.Thens:
                    specificAlt.postCondition += sentence.normalContent
                rucm.specificAlt.append(specificAlt)
            elif taggedGWT.flowType == 'bounded':
                boundedAlt = BoundedFlow()
                boundedAlt.rfs = [num + 1 for num in taggedGWT.refer]
                boundedAlt.actions = [sentence.normalContent for sentence in
                                      taggedGWT.Whens]  # TODO 选择的action范围
                for refer in taggedGWT.refer:
                    sent=rucm.basic.actions[refer]
                    #sent=sent.replace(action, 'VALIDATES THAT')
                    sent='系统 VALIDATES THAT '+sent
                    rucm.basic.actions[refer]=sent
                for sentence in taggedGWT.Thens:
                    boundedAlt.postCondition += sentence.normalContent
                rucm.boundedAlt.append(boundedAlt)
            elif taggedGWT.flowType == 'global':
                globalAlt = GlobalFlow()
                globalAlt.condition = taggedGWT.condition.originContent
                globalAlt.actions = [sentence.normalContent for sentence in taggedGWT.Whens]
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
    from response.gwtresponse import GWTImporter
    #from rucmresponse import RUCMGnerator

    nlp = NLPExecutor()
    importer = GWTImporter(nlp)
    gwtlist = importer.importGWT(filepath=r'D:\StarUMLWorkspace\GWT2RUCM\Project\GWT2RUCM_Pyltp\testfile\new_input_demo.gwtfile')
    generator = RUCMGnerator(nlp)
    generator.generateRUCMs(gwtlist)
