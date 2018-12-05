import re


class LableGenerator():
    '''
    nlpExecutor:nlp工具类实例，由上层传入
    '''

    def __init__(self, nlpExecutor):
        self.nlp = nlpExecutor

    '''
    param：
        gwtList:未标签化的gwt的list，每个元素的类型为TaggedGWT,由上层传入
    return：
        修改对象，不返回新值
    '''

    def generateLable(self, gwtList):
        self.__simpleLable(gwtList)
        pass

    '''
    检索关键词语句并标记，包括Actor,UseCaseName，INCLUDE,EXTEND,
    include和extend层次上更偏向已标记，故此处暂只识别usecasename
    此外对含global的标记flowtype
    '''

    def __simpleLable(self, gwtList):
        for gwt in gwtList:
            story = gwt.Features[0].content
            content = re.match(r'.*As\sa\s*([\u4e00-\u9fa5\u3001]+)\uff0c?,?\s?([\u4e00-\u9fa5]+).*', story)
            actorContent = content.group(1)
            gwt.useCaseName = content.group(2)
            actors = actorContent.split('\u3001')
            gwt.PrimaryActor = actors[0]
            if len(actors) > 1:
                gwt.SecondaryActors = ''
                for actor in actors[1:]:
                    gwt.SecondaryActors += actor
            for sentence in gwt.Givens:
                if sentence.type == 'precondition':
                    content = sentence.content
                    if re.match('.*GLOBAL.*', content):
                        gwt.flowType = 'global'
                        break

    def __normalize(self):
        pass

    '''
    判断flowType，global已知，暂认为basic为第一个，
    specific与basic的precondition只有一个不一样，从action不同判断rfs
    除以上剩下的即为bounded，从action两端判断rfs 
    同时取得commonPrec作为rucm的precondition
    '''

    def __addGWTLable(self, gwtList):
        basic = gwtList[0]
        basic.flowType = 'basic'
        for gwt in gwtList[1:]:
            if gwt.flowType != 'global':
                diff = []
                for i in range(0, len(basic.Givens) - 1):
                    similarity = self.nlp.similarity(basic.Givens[i].content,
                                                     gwt.Givens[i].content)
                    if similarity > 0.8 and similarity < 1:
                        diff.append(i)
                if len(diff) == 1:
                    gwt.flowType = 'specific'
                    for i in range(0, len(basic.Whens) - 1):
                        similarity = self.nlp.similarity(basic.Whens[i].content,
                                                         gwt.Whens[i].content)
                        if similarity != 1:
                            gwt.BranchScenarios = [diff[0],i + 1]#diff[0]指示分支condition，i+1指示分支action
                else:
                    gwt.flowType = 'bounded'
                    i = 0
                    j = len(basic.Whens) - 2
                    while i < j:
                        if self.nlp.similarity(basic.Whens[i], gwt.Whens[i]) == 1:
                            i += 1
                        else:
                            break
                    while i < j:
                        if self.nlp.similarity(basic.Whens[j], gwt.Whens[j]) == 1:
                            j -= 1
                        else:
                            break
                    gwt.BranchScenarios = [i, j]
        preList = [gwt for gwt in gwtList[1:] if gwt.flowType != 'global']
        basic.commonPrec = ''
        for i in range(0, len(basic.Givens) - 1):
            common = True
            for gwt in preList:
                if basic.Givens[i] != gwt.Givens[i]:
                    common = False
                    break
            if common:
                basic.commonPrec += basic.Givens[i]
