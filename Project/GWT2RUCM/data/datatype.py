class GWT(object):
    __slots__ = ('gwt_id', 'Scenario', 'Features', 'Givens', 'Whens', 'Thens')


class TaggedGWT(GWT):
    __slots__ = (
        'useCaseName', 'PrimaryActor', 'SecondaryActors', 'BranchScenarios', 'preScenarios', 'postScenarios',
        'flowType', 'commonPrec')

    def __init__(self):
        self.PrimaryActor = 'None'
        self.SecondaryActors = 'None'
        self.preScenarios = None
        self.postScenarios = None
        self.flowType = None


class RUCM():
    __slots__ = ('useCaseName', 'briefDescription', 'precondition', 'primaryActor', 'secondaryActors', 'dependency',
                 'generalization', 'basic', 'specificAlt', 'boundedAlt', 'globalAlt')

    def __init__(self, name):
        self.useCaseName = name

    def __str__(self):
        basicStr = 'Basic Flow:\n'
        for i in range(0, len(self.basic.actions)):
            basicStr += str(i + 1) + '.' + self.basic.actions[i] + '\n'
        basicStr += 'postcondition:' + self.basic.postCondition + '\n'
        specStr = ''
        if len(self.specificAlt) > 0:
            for spec in self.specificAlt:
                specStr += 'Specific Alternative Flow: RFS ' + str(spec.rfs) + '\n'
                for i in range(0, len(spec.actions)):
                    specStr += str(i + 1) + '.' + spec.actions[i] + '\n'
                specStr += 'postcondition:' + spec.postCondition + '\n'
        bounStr = ''
        if len(self.boundedAlt) > 0:
            for boun in self.boundedAlt:
                bounStr += 'Bounded Alternative Flow: RFS ' + str(boun.rfs[0]) + '-' + str(
                    boun.rfs[-1]) + '\n'  # TODO rfs如何获得
                for i in range(0, len(boun.actions)):
                    bounStr += str(i + 1) + '.' + boun.actions[i] + '\n'
                bounStr += 'postcondition:' + boun.postCondition + '\n'
        globStr = ''
        if len(self.globalAlt) > 0:
            for glob in self.globalAlt:
                globStr += 'Global Alternative Flow: IF ' + glob.condition + '\n'
                for i in range(0, len(glob.actions)):
                    globStr += str(i + 1) + '.' + glob.actions[i] + '\n'
                globStr += 'END IF\npostcondition:' + glob.postCondition + '\n'
        result = 'Use Case Name: ' + self.useCaseName + '\n' + 'Brief Description: ' \
                 + self.briefDescription + '\n'
        result += 'Precondition: ' + self.precondition + '\n' + 'Primary Actor:' + \
                  self.primaryActor + '\n' + 'Secondary Actors:' + self.secondaryActors + '\n'
        result += 'Dependency:' + self.dependency + '\n' + 'Generalization:' + self.generalization + '\n'
        result += basicStr + specStr + globStr
        return result
        '''
        return 'Use Case Name: ' + self.useCaseName + '\n ' + 'Brief Description: ' \
               + self.briefDescription + '\n', +'Precondition: ' + self.precondition + '\n' \
               + 'Primary Actor:' + self.primaryActor + '\n' + 'Secondary Actors:' + \
               +self.secondaryActors + '\n' + 'Dependency:' + self.dependency + '\n'

        #       + 'Generalization:' + self.generalization \
               #+ '\n' + basicStr+specStr+globStr
        '''


class Sentence(object):
    __slots__ = ('sentence_id', 'stype', 'content', 'sequence')

    def __init__(self, stype=None, content=None, sequence=None):
        if stype is not None:
            self.stype = stype
        if content is not None:
            self.content = content
        if sequence is not None:
            self.sequence = sequence


class TaggedSentence(Sentence):
    __slots__ = ('secondType', 'associations')


class Association(object):
    __slots__ = ('gwtId', 'sentenceId', 'connect_type')


class Scenario(object):
    __slots__ = ('gwtId', 'conditionIds')


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
