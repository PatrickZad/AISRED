from data.datatype import GWT, Sentence
import re


class GWTImporter():
    def __init__(self, nlpExecutor=None):
        self.nlpTool = nlpExecutor

    def importGWT(self, filepath=None, filecontent=None):
        text = None
        if filecontent is not None:
            text = filecontent
        elif filepath is not None:
            with open(file, 'r', encoding='utf-8') as f:
                text = f.read()
        if text is not None:
            gwtTextList = text.split('Story:')[1:]
            for gwtText in gwtTextList:
                gwtText = gwtText.replace('\n', '')
                contentGroup = re.match('\s*(.*)\s*Scenario:\s*(.*)\s*Business\sRule:\s*(.*)'
                                        'Given:\s*Preconditions:\s*(.*)\s*Fixed\sdata:\s*(.*)'
                                        'When:\s*Action:\s*(.*)\s*Input\sdata:\s*(.*)'
                                        'Then:\s*Output\sdata:\s*(.*)\s*Postcondition:\s*(.*)\s*', gwtText)
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



if __name__ == '__main__':
    from support.nlpsupport import NLPExecutor

    file = r'../testfile/inputdemo.gwtfile'
    tool = NLPExecutor(r'../stanford-corenlp-full-2018-10-05')
    importer = GWTImporter(tool)
    # importer = GWTImporter()
    importer.importGWT(filepath=file)
    tool.nlp.close()
