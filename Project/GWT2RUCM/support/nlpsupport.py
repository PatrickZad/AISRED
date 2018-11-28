from stanfordcorenlp import StanfordCoreNLP
class NLPExecutor():
    def __init__(self):
        self.nlp=StanfordCoreNLP(r'./stanford-corenlp-full-2018-10-05',lang='zh')
    def wordTokenize(self,sentance):
        //TODO
    def posTag(self,sentance):
        //TODO
    def dictUpdate(self,wordDict):
        //TODO
    def anaphoraResolution(self,text):
        //TODO
    def sentComposite(self,text):
        //TODO
    def featureExtract(self,text):
        //TODO