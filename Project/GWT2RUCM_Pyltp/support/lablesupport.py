import re
from data.datatype import TaggedGWT, Sentence


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
        for i in range(len(gwtList)):
            gwtList[i] = TaggedGWT(gwtList[i])
        self.__simpleLable(gwtList)
        self.__addGWTLable(gwtList)
        return gwtList

    '''
    标记基础标签
    GWT级:usecase,flowType的basic和bunded
    句子级:wordlist,actor,action
    '''

    def __simpleLable(self, gwtList):
        conditionsum = [len(gwt.Givens) for gwt in gwtList]
        conditionsum.sort()
        for gwt in gwtList:
            if len(gwt.Givens) == conditionsum[0]:
                gwt.flowType = 'basic'
                self.basic = gwt
                break
        for gwt in gwtList:
            gwt.useCaseName = gwt.Feature
            for sent in gwt.Scenario:
                sent.wordlist = self.nlp.wordTokenize(sent.originContent)
                parselist = self.nlp.parse(sent.wordlist)
                for i in range(len(parselist)):
                    if parselist[i].relation == 'SBV':
                        sent.actor = i
                        sent.action = parselist[i].head - 1
                        break
            for sent in gwt.Givens:
                sent.wordlist = self.nlp.wordTokenize(sent.originContent)
                parselist = self.nlp.parse(sent.wordlist)
                for i in range(len(parselist)):
                    if parselist[i].relation == 'SBV':
                        sent.actor = i
                        sent.action = parselist[i].head - 1
                        break                
            for sent in gwt.Whens:
                sent.wordlist = self.nlp.wordTokenize(sent.originContent)
                parselist = self.nlp.parse(sent.wordlist)
                for i in range(len(parselist)):
                    if parselist[i].relation == 'SBV':
                        sent.actor = i
                        sent.action = parselist[i].head - 1
                        break
            for sent in gwt.Thens:
                sent.wordlist = self.nlp.wordTokenize(sent.originContent)
                parselist = self.nlp.parse(sent.wordlist)
                for i in range(len(parselist)):
                    if parselist[i].relation == 'SBV':
                        sent.actor = i
                        sent.action = parselist[i].head - 1
                        break
            if gwt is not self.basic:
                if len(gwt.Givens) - len(self.basic.Givens) > 1:
                    gwt.flowType = 'bounded'


    '''
    标记高级标签，包括
    GWT级:refer,condition,flowtype的specific和global
    句子级:nomalContent,type,associated
    '''

    def __addGWTLable(self, gwtList):
        for gwt in gwtList:
            addition=[]
            index=None
            for i in range(0,len(gwt.Whens)):
                sent=gwt.Whens[i]
                sent.normalContent=''
                parse = self.nlp.parse(sent.wordlist)
                if self.nlp.isSimple(parse):
                    sent.type = 'normal'
                elif sent.wordlist.count('如果') > 0:
                    sent.type = 'conditional'
                elif sent.wordlist.count('直到')>0:
                    sent.type='circular'
                    index=i
                    textsents=sent.originContent.split('，')
                    addition=[Sentence(text) for text in textsents]
                    for sent in addition:
                        sent.wordlist=self.nlp.wordTokenize(sent.originContent)
                        parselist = self.nlp.parse(sent.wordlist)
                        sent.normalContent=''
                        sent.type='normal'
                        for i in range(len(parselist)):
                            if parselist[i].relation == 'SBV':
                                sent.actor = i
                                sent.action = parselist[i].head - 1
                                break
                    addition[0].normalContent='DO '
                else:
                    sent.type = 'normal'
            if index is not None:
                temp=gwt.Whens[0:index]+addition
                gwt.Whens=temp+gwt.Whens[index+len(addition):]
            for sent in gwt.Whens:
                self.nlp.normalize(sent)
            for sent in gwt.Thens:
                sent.wordlist = self.nlp.wordTokenize(sent.originContent)
                parse = self.nlp.parse(sent.wordlist)
                sent.type='then'
                self.nlp.normalize(sent, parse)
            if gwt is self.basic:
                for sent in gwt.Givens:
                    sent.type = 'common'
            elif gwt.flowType == 'bounded':
                gwt.condition = []
                gwt.refer=[]
                for sent in gwt.Givens:
                    if self.nlp.maxSimilarity(self.basic.Givens, sent)[1] > 0.99:
                        sent.type = 'common'
                    else:
                        sent.type = 'unique'
                        gwt.condition.append(sent)       
                sentlist=self.basic.Whens.copy()
                for sent in gwt.condition:
                    index, similarity = self.nlp.maxSimilarity(sentlist, sent)
                    if similarity > 0.5:
                        sent.associated = index
                        gwt.refer.append(index)
                        sentlist[index].originContent=''

            else:
                gwt.condition = []
                for sent in gwt.Givens:
                    if self.nlp.maxSimilarity(self.basic.Givens, sent)[1] > 0.99:
                        sent.type = 'common'
                    else:
                        sent.type = 'unique'
                        gwt.condition.append(sent)
                index, similarity = self.nlp.maxSimilarity(self.basic.Whens, sent)
                if similarity > 0.6:
                    sent.associated = index
                    gwt.flowType = 'specific'
                    gwt.refer=index
                else:
                    gwt.flowType = 'global'
