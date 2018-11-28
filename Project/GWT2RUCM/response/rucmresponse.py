from support.lablesupport import LableGenerator
from support.nlpsupport import NLPExecutor
class RUCMGnerator():
    def __init__(self):
        self.nlp=NLPExecutor()
        self.lable=LableGenerator(self.nlp)
        //TODO