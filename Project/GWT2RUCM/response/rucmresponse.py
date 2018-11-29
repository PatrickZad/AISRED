from support.lablesupport import LableGenerator
from support.nlpsupport import NLPExecutor
class RUCMGnerator():
    def __init__(self):
        self.nlp=NLPExecutor()
        self.lable=LableGenerator(self.nlp)
    def generateRUCMs(self):
        '''
        根据id获取要处理的GWT
        为这一组GWT添加标签获得一组TaggedGWT
        将这一组TaggedGWT合成一组RUCM
        '''