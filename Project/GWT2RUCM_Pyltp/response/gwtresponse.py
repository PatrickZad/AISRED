from data.datatype import GWT, Sentence
import re


class GWTImporter():
    def __init__(self, nlpExecutor):
        self.nlpTool = nlpExecutor

    '''
    param:
        filepath:文件路径
        filecontent:文件的str
    return:
        gwt的list，其中各句只有originContent
    '''

    def importGWT(self, filepath=None, filecontent=None):
        text = None
        if filecontent is not None:
            text = filecontent
        elif filepath is not None:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        if text is not None:
            gwtlist = []
            gwtTextList = text.split('Feature:')[1:]
            for gwtText in gwtTextList:
                gwtText = gwtText.replace('\n', '')  # TODO 如果那么，做直到等复合句可以不分行但标点要正确不分句
                contentGroup = re.match('\s*([\u4e00-\u9fa5]*).*Scenario:\s*(.*)\s*Given:\s*(.*)\s*'
                                        'When:\s*(.*)\s*Then:\s*(.*)\s*', gwtText)
                originGWT = GWT()
                originGWT.Feature = contentGroup.group(1)
                originGWT.Scenario = []
                originGWT.Givens = []
                originGWT.Whens = []
                originGWT.Thens = []
                sentList = self.nlpTool.splitSentences(contentGroup.group(2))
                for sent in sentList:
                    cons = sent.split('或')  # 多条件切分，对分句的补充
                    allSent=True
                    for con in cons:
                        if len(con)>1 and not self.nlpTool.isSimple(self.nlpTool.parse(text=con)):
                            allSent=False
                    for con in cons:
                        if len(con) > 1:
                            sentence = Sentence(sent)
                            originGWT.Scenario.append(sentence)
                sentList = self.nlpTool.splitSentences(contentGroup.group(3))
                for sent in sentList:
                    sentence = Sentence(sent)
                    originGWT.Givens.append(sentence)
                sentList = self.nlpTool.splitSentences(contentGroup.group(4))
                for sent in sentList:
                    sentence = Sentence(sent)
                    originGWT.Whens.append(sentence)
                sentList = self.nlpTool.splitSentences(contentGroup.group(5))
                for sent in sentList:
                    sentence = Sentence(sent)
                    originGWT.Thens.append(sentence)
                gwtlist.append(originGWT)
            return gwtlist


if __name__ == '__main__':
    pass
