from stanfordcorenlp import StanfordCoreNLP


class NLPExecutor():
    def __init__(self, path):
        self.nlp = StanfordCoreNLP(path, lang='zh')

    def wordTokenize(self, sentence):
        pass

    def posTag(self, sentence):
        pass

    def dictUpdate(self, wordDict):
        pass

    def anaphoraResolution(self, text):
        pass

    def sentComposite(self, text):
        pass

    def featureExtract(self, text):
        pass
