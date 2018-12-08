from support.datasupport import *
class BackgroundImporter():
    '''
    将领域背景信息文件导入数据库，当需要进行生成RUCM操作时才使用领域背景信息创建自然语言处理器
    '''

    def __init__(self, file,):
        self.inputFile = file

    def importBackground(self, fileText, filePath):
        with open(filePath, 'w', encoding='utf-8') as f:
            f.write(fileText)
