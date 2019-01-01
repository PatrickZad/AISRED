import os
from pyltp import Segmentor, SentenceSplitter, Postagger, Parser
from textrank4zh import TextRank4Sentence
import ast
from gensim import corpora
from gensim.similarities import Similarity

ltpBase = './ltp_data'
cwsPath = os.path.join(ltpBase, 'cws.model')
posPath = os.path.join(ltpBase, 'pos.model')
parserPath = os.path.join(ltpBase, 'parser.model')


class NLPExecutor:
    def __init__(self):
        self.seg = Segmentor()
        self.seg.load(cwsPath)
        self.pos = Postagger()
        self.pos.load(posPath)
        self.parser = Parser()
        self.parser.load(parserPath)
        self.tr = TextRank4Sentence()
    '''
    param:
        text:输入文本
    return:
        摘要的句子list
    '''
    def generateSummary(self, text):
        # TODO 摘要生成实现方法待改进
        self.tr.analyze(text=text)
        return self.tr.get_key_sentences(num=1)


    '''
    param:
        text:输入文本
    return:
        分句的句子list
    '''


    def splitSentences(self, text):
        return list(SentenceSplitter.split(text))


    '''
    param:
        sent1,sent2:两个句子
    return:
        两个句子的相似度
    '''


    def similarity(self, sent1, sent2):
        if sent1=='' or sent2=='':
            return 0
        text1 = self.wordTokenize(sent1)
        text2 = self.wordTokenize(sent2)
        texts = [text1, text2]
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        similarity = Similarity('-Similarity-index', corpus, num_features=len(dictionary))
        return similarity[dictionary.doc2bow(text1)][1]


    # TODO VALIADATES THAT添加放在RUCM生成层
    '''
    def addValidate(self,sentence):
        tokens=self.wordTokenize(sentence)
        tokens[1]='VALIDATES THAT'
        return ''.join(tokens)
    '''
    '''
    param:
        sentence:一个句子
    return:
        分词词链，list，标点符号会被作为一个词
    '''


    def wordTokenize(self, sentence):
        return list(self.seg.segment(sentence))


    '''
    param:
        sentence:一个句子
        wordlist:分词词链
    return:
        仅有词性标注的词性链，index与分词词链对应
    '''


    def posTag(self, sentence=None, wordlist=None):
        if sentence is not None:
            wordlist = list(self.seg.segment(sentence))
        return list(self.pos.postag(wordlist))


    '''
    param:
        sentence:分词词典的文件路径，每个词独占一行的纯文本文件
        wordlist:标注词典的文件路径，每个词及其词性占一行，词与词性标注之间空格分隔，可以有多个词性
    return:
        无
    '''


    def dictUpdate(self, segDict=None, posDict=None):
        if segDict is not None:
            self.seg.load_with_lexicon(cwsPath, segDict)
        if posDict is not None:
            self.pos.load_with_lexicon(posPath, posDict)


    '''
    param:
        sentence:原始句子
        wordlist:句子的分词词链
        poslist:词性标注词链
    return:
        依存句法分析结果
    '''


    def parse(self, wordlist=None,text=None):
        if text is not None:
            wordlist=self.wordTokenize(text)
        poslist = self.posTag(wordlist=wordlist)
        return list(self.parser.parse(wordlist, poslist))


    '''
    param:
        sentence:Sentence对象
        parselist:依存句法分析结果
    return:
        规范化句式之后的句子
    '''


    def normalize(self, sentence, parselist=None):  # TODO 效果在调试时继续调整):
        wordlist=sentence.wordlist
        poslist=self.posTag(wordlist=wordlist)
        if parselist is None:
            parselist = self.parse(wordlist=wordlist, poslist=poslist)
        # TODO 替换IF,ELSE,THEN,DO,UNTIL
        #if sentence.type == 'conditional':
            # TODO
        for i in range(0,len(wordlist)):
            if wordlist[i] == '如果':
                wordlist[i]='IF'
            elif wordlist[i]=='那么':
                wordlist[i]='THEN'
            elif wordlist[i]=='否则':
                wordlist[i]='ELSE'
        #elif sentence.type == 'circular':
            # TODO
        for i in range(0,len(wordlist)):
            if wordlist[i] == '直到':
                wordlist[i]='UNTIL'
            #wordlist=['DO']+wordlist
        for i in range(0,len(wordlist)):
            if wordlist[i] == '同时':
                wordlist[i]='MEANWHILE'
        newWords = wordlist.copy()
        #TODO 去量词效果
        '''
        if sentence.type=='normal':
            for i in range(len(wordlist)-1, -1, -1):
                if parselist[i].relation == 'ATT' and (poslist[i] == 'm' or poslist[i] == 'q'):
                    del newWords[i]
        if sentence.normalContent is None:
            sentence.normalContent='''''
        for word in newWords:
            sentence.normalContent+=word
        '''
        if sentence.type=='circular':
            sentence.normalContent='DO'+sentence.normalContent
        
        if sentence.type=='circular':
            sentence.normalContent='DO'+sentence.normalContent
            for i in range(0,len(wordlist)):
                if wordlist[i] == '直到':
                    wordlist[i]='UNTIL'
        '''


    '''
    param:
        parselist:依存句法分析结果
    return:
        是否为简单句
    '''


    def isSimple(self, parselist):
        count = 0
        for parse in parselist:
            if parse.relation == 'SBV':
                count += 1
        if count == 1:
            return True
        else:
            return False


    '''
    param:
        sentlist:句子集合
        sent:单个句子
    return:
        sentlist中与sent相似度最高的句子的索引与相似度
    '''


    def maxSimilarity(self, sentlist, sent):
        max = [-1, -1]
        for i in range(len(sentlist)):
            similarity = self.similarity(sentlist[i].originContent, sent.originContent)
            if similarity > max[1]:
                max = [i, similarity]
        return max
if __name__=='__main__':
    sent1='该卡为有效卡'
    sent2='该卡为无效卡'
    nlp=NLPExecutor()
    nlp.dictUpdate('./newword')
    print(nlp.similarity(sent1,sent2))

