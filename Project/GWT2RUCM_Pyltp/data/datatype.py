class GWT(object):
    __slots__ = ('Scenario', 'Feature', 'Givens', 'Whens', 'Thens')


class TaggedGWT(GWT):
    '''
    refer为异常操作索引，condition为异常发生条件
    '''
    __slots__ = ('useCaseName','flowType','refer','condition')

    def __init__(self,gwt):
        self.Feature=gwt.Feature
        self.Scenario=gwt.Scenario
        self.Givens=gwt.Givens
        self.Whens=gwt.Whens
        self.Thens=gwt.Thens
        self.flowType=''
        self.refer=''
        self.condition=''
    def scenarioStr(self):
        scenariolist=[sent.originContent for sent in self.Scenario]
        scenario=''
        for scen in scenariolist:
            scenario+=scen
        return scenario
    def __str__(self):
        scenariostr='\t[Scenarion]\n'
        for sent in self.Scenario:
            scenariostr+=sent.__str__('\t\t')
        givenstr='\t[Given]\n'
        for sent in self.Givens:
            givenstr+=sent.__str__('\t\t')   
        whenstr='\t[When]\n'
        for sent in self.Whens:
            whenstr+=sent.__str__('\t\t')
        thenstr='\t[Then]\n'
        for sent in self.Thens:
            thenstr+=sent.__str__('\t\t')
        result='[UseCaseName]'+self.useCaseName+'\n\t[FlowType]'+self.flowType+'\n\t[Refer]'+str(self.refer)+'\n\t[Condition]'+str([sent.originContent for sent in self.condition if isinstance(self.condition,list)])
        result+='\n\t[Feature]'+self.Feature+'\n'+scenariostr+givenstr+whenstr+thenstr
        return result

class RUCM():
    __slots__ = ('useCaseName', 'briefDescription', 'precondition', 'primaryActor', 'secondaryActors', 'dependency',
                 'generalization', 'basic', 'specificAlt', 'boundedAlt', 'globalAlt')

    def __init__(self, name):
        self.useCaseName = name

    def __str__(self):
        basicStr = '\tBasic Flow:\n'
        for i in range(0, len(self.basic.actions)):
            basicStr +='\t\t'+ str(i + 1) + '.' + self.basic.actions[i] + '\n'
        basicStr += '\t\tpostcondition:' + self.basic.postCondition + '\n'
        specStr = ''
        if len(self.specificAlt) > 0:
            for spec in self.specificAlt:
                specStr += '\tSpecific Alternative Flow: RFS ' + str(spec.rfs) + '\n'
                for i in range(0, len(spec.actions)):
                    specStr +='\t\t' +str(i + 1) + '.' + spec.actions[i] + '\n'
                specStr += '\t\t'+str(len(spec.actions)+1)+'.ABORT\n'+'\t\tpostcondition:' + spec.postCondition + '\n'
        bounStr = ''
        if len(self.boundedAlt) > 0:
            for boun in self.boundedAlt:
                bounStr += '\tBounded Alternative Flow: RFS ' + str(boun.rfs)[1:-1] + '\n'  # TODO rfs如何获得
                for i in range(0, len(boun.actions)):
                    bounStr +='\t\t'+ str(i + 1) + '.' + boun.actions[i] + '\n'
                bounStr += '\t\tpostcondition:' + boun.postCondition + '\n'
        globStr = ''
        if len(self.globalAlt) > 0:
            for glob in self.globalAlt:
                globStr += '\tGlobal Alternative Flow: IF ' + glob.condition + '\n'
                for i in range(0, len(glob.actions)):
                    globStr +='\t\t'+ str(i + 1) + '.' + glob.actions[i] + '\n'
                globStr += '\t\tEND IF\n\t\tpostcondition:' + glob.postCondition + '\n'
        result = 'Use Case Name: ' + self.useCaseName + '\n' + '\tBrief Description: ' \
                 + self.briefDescription + '\n'
        result += '\tPrecondition: ' + self.precondition + '\n' + '\tPrimary Actor:' + \
                  self.primaryActor + '\n' + '\tSecondary Actors:' + str(self.secondaryActors[0])[1:-1] + '\n'
        result += '\tDependency:' + self.dependency + '\n' + '\tGeneralization:' + self.generalization + '\n'
        result += basicStr + specStr + bounStr+globStr
        return result


class Sentence(object):
    '''
    originContent为原始句子，actor为动作实施者索引，action为句子谓词索引，
    wordlist为句子词链，normalContent为调整后的句子,
    type指示when中句子为普通action-'normal'，条件action-'conditional'或循环action-'circular',
        或given中句子为共同前提-'common'或异常前提-'unique'
    在given中associated指示unique异常前提所来自的操作索引
    '''
    __slots__ = ('originContent', 'actor', 'action',
     'wordlist','normalContent','type','associated')

    def __init__(self, originContent):
        self.originContent=originContent
        self.actor=None
        self.action=''
        self.type=''
        self.associated=''
        self.normalContent=''
        self.wordlist=''
    def __str__(self,indent):
        sentstr=indent+'[originContent]'+self.originContent+'\n'
        sentstr+=indent+'\t[wordlist]'+str(self.wordlist)+'\n'
        sentstr+=indent+'\t[actor]'+str(self.actor)+'\n'
        sentstr+=indent+'\t[action]'+str(self.action)+'\n'
        sentstr+=indent+'\t[normalContent]'+str(self.normalContent)+'\n'
        sentstr+=indent+'\t[type]'+str(self.type)+'\n'
        sentstr+=indent+'\t[associated]'+str(self.associated)+'\n'
        return sentstr

class BasicFlow():
    def __init__(self):
        self.actions = []
        self.postCondition = ''

    def addAction(self, action):
        self.actions.append(action)


class SpecificFlow():
    def __init__(self):
        self.rfs = 0
        self.actions = []
        self.postCondition = ''

    def addAction(self, action):
        self.actions.append(action)


class BoundedFlow():
    def __init__(self):
        self.rfs = []
        self.actions = []
        self.postCondition = ''

    def addRFS(self, num):
        self.rfs.append(num)

    def addAction(self, action):
        self.actions.append(action)


class GlobalFlow():
    def __init__(self):
        self.condition = ''
        self.actions = []
        self.postCondition = ''

    def addAction(self, action):
        self.actions.append(action)
