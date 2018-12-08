from stanfordcorenlpTool import StanfordCorenlpTool
from textrank4zh import TextRank4Sentence
import ast
from gensim import corpora
from gensim.similarities import Similarity
import jieba
import re


class nlpToolExecutor():
    def __init__(self, path):
        self.nlpToolTool = StanfordCorenlpTool(path, lang='zh')
        self.tr = TextRank4Sentence()

    def firstNamedEntities(self, sentence):
        return self.nlpToolTool.ner(sentence)[0][0]

    '''
    param:
        text:输入文本
    return:
        摘要的句子list
    '''

    def generateSummary(self, text):
        # TODO 摘要生成实现方法待选
        self.tr.analyze(text=text)
        return self.tr.get_key_sentences(num=1)

    def splitSentences(self, text):
        sentenceList = ast.literal_eval(self.nlpTool.annotate(text, properties={'ssplit'}))['sentences']
        resultList = []
        for item in sentenceList:
            for token in item['tokens']:
                if len(token['word']) > 1:
                    resultList.append(token['word'])
        return resultList
    def similarity(self,sent1,sent2):
        text1 = self.wordTokenize(sent1)
        text2 = self.wordtokenize(sent2)
        texts = [text1, text2]
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        similarity = Similarity('-Similarity-index', corpus, num_features=len(dictionary))
        return similarity[dictionary.doc2bow(text1)][1]
    def addValidate(self,sentence):
        tokens=self.wordTokenize(sentence)
        tokens[1]='VALIDATES THAT'
        return ''.join(tokens)
    def wordTokenize(self, sentence):
        return self.nlpTool.word_tokenize(sentence)

    def posTag(self, sentence):
        return self.nlpTool.pos_tag(sentence)

    def dictUpdate(self, wordDict):
        self.wordDict=wordDict
        jieba.load_userdict(wordDict)

    def anaphoraResolution(self, text):
        pass

    def sentComposite(self, text):
        pass

    def featureExtract(self, text):
        pass
