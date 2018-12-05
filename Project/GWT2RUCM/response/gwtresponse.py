from data.datatype import GWT, Sentence
import re


class GWTImporter():
    def __init__(self, dataDispatcher, nlpExecutor):
        self.dataTool = dataDispatcher
        self.nlpTool = nlpExecutor

    def importGWT(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
        gwtTextList = text.split('Story:')[1:]
        for gwtText in gwtTextList:
            contentGroup = re.match(r'(.*)Scenario:\s*\n*(.*)Business\sRule:\s*\n*(.*) \
                            Given:\nPreconditions:\s*\n*(.*)Fixed\sdata:\s*\n*(.*) \
                            When:\nAction:\s*\n*(.*)Input\sdata:\s*\n*(.*)\nThen:\n \
                            Output\sdata:\s*\n*(.*)\nPostcondition:\s*\n*(.*)\n+', gwtText)
            originGWT = GWT()
            originGWT.Features = []
            originGWT.Scenario = contentGroup.group(2)
            originGWT.Givens = []
            originGWT.Whens = []
            originGWT.Thens = []
            sentence = Sentence(stype='story', content=contentGroup.group(1))
            originGWT.Features.append(sentence)
            sentence = Sentence(stype='business_rule', content=contentGroup.group(3))
            originGWT.Features.append(sentence)
            sentList = self.nlpTool.splitSentences(contentGroup.group(4))
            for item in sentList:
                sentence = Sentence(stype='precondition', content=item)
                originGWT.Givens.append(sentence)
            sentence = Sentence(stype='fixed_data', content=contentGroup.group(5))
            originGWT.Givens.append(sentence)
            sentList = self.nlpTool.splitSentences(contentGroup.group(6))
            for i in range(0, len(sentList)):
                sentence = Sentence(stype='action', content=sentList[i], sequence=i + 1)
                originGWT.Whens.append(sentence)
            sentence = Sentence(stype='inputdata', content=contentGroup.group(7))
            originGWT.Whens.append(sentence)
            sentence = Sentence(stype='outputdata', content=contentGroup.group(8))
            originGWT.Thens.append(sentence)
            sentList = self.nlpTool.splitSentences(contentGroup.group(9))
            for item in sentList:
                sentence = Sentence(stype='postcondition', content=item)
                originGWT.Thens.append(sentence)
            self.dataTool.insertGWT(originGWT)
