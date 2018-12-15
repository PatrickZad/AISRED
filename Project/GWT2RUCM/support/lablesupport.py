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
        self.__addGWTLable(gwtList)
        return gwtList

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
                    gwt.SecondaryActors += actor + ' '
            for sentence in gwt.Givens:
                if sentence.stype == 'precondition':
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
    使用BranchScenarios属性储存rfs
    '''

    def __addGWTLable(self, gwtList):
        # TODO bounded的rfs判断需要修改
        basic = gwtList[0]
        basic.flowType = 'basic'
        for gwt in gwtList[1:]:
            if gwt.flowType != 'global':
                nega = []
                diff = []
                simiList = []
                for i in range(0, len(gwt.Givens) - 1):
                    for sentence in basic.Givens[:-1]:
                        simiList.append(self.nlp.similarity(gwt.Givens[i].content,
                                                            sentence.content))
                    simiList.sort()
                    if simiList[-1] > 0.8 and simiList[-1] < 0.99:
                        nega.append(i)
                    elif simiList[-1] <= 0.8:
                        diff.append(i)
                    simiList = []
                if len(nega) == 1 or len(diff) == 1:
                    gwt.flowType = 'specific'
                    for i in range(0, len(basic.Whens) - 1):
                        similarity = self.nlp.similarity(basic.Whens[i].content,
                                                         gwt.Whens[i].content)
                        if similarity < 0.99 and similarity > 0.8:
                            gwt.BranchScenarios = [nega[0], i + 1]  # nega[0]指示分支condition来自分支gwt，i+1指示分支action来自basic
                            break
                else:
                    gwt.flowType = 'bounded'
                    gwt.BranchScenarios = []
                    for i in range(0, len(basic.Whens) - 2):  # 找到action开始不同的地方
                        if self.nlp.similarity(basic.Whens[i].content, gwt.Whens[i].content) > 0.99:
                            i += 1
                        else:
                            break
                    # 比较nega的action和precondition
                    for j in diff:
                        for k in range(i, len(basic.Whens) - 2):
                            sent0 = basic.Whens[k].content
                            sent1 = gwt.Givens[j].content
                            similarity = self.nlp.similarity(sent0, sent1)  # 找出basic里与gwt的pre相近的action
                            if similarity > 0.4 and similarity < 0.99:
                                gwt.BranchScenarios.append(k + 1)
                    gwt.BranchScenarios = list(set(gwt.BranchScenarios))
                    gwt.BranchScenarios.sort()

                    '''
                    while i < j:
                        if self.nlp.similarity(basic.Whens[j], gwt.Whens[j]) == 1:
                            j -= 1
                        else:
                            break
                    gwt.BranchScenarios = [i, j]
                    '''
        preList = [gwt for gwt in gwtList[1:] if gwt.flowType != 'global']
        basic.commonPrec = ''
        for i in range(0, len(basic.Givens) - 1):
            common = True
            for gwt in preList:
                if basic.Givens[i].content != gwt.Givens[i].content:
                    common = False
                    break
            if common:
                basic.commonPrec += basic.Givens[i].content + '。'
