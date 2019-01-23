
class BackgroundImporter():
    def __init__(self, nlp):
        self.nlp=nlp

    def importBackground(self,segDict=None, posDict=None):
        self.nlp.dictUpdate(segDict,posDict)
