class GWT(object):
    __slots__ = ('gwt_id', 'Scenario', 'Features', 'Givens', 'Whens', 'Thens')


class TagedGWT(GWT):
    __slots__ = ('useCaseName', 'BranchScenarios', 'preScenarios', 'postScenarios', 'flowType')
class RUCM():
    __slots__=('useCaseName','briefDescription','precondition','primaryActor','secondaryActors','dependency','generalization','basic','specific','bounded','global')
    def __init__(self,name):
        self.useCaseName=name


class Sentence(object):
    __slots__ = ('sentence_id', 'type', 'content', 'sequence')


class TagedSentence(Sentence):
    __slots__ = ('secondType', 'associations')


class Association(object):
    __slots__ = ('gwtId', 'sentenceId', 'connect_type')


class Scenario(object):
    __slots__ = ('gwtId', 'conditionIds')

class BasicFlow():
    def __init__(self):
        self.actions=[]
        self.postCondition=''
    def addAction(action):
        self.actions.append(action)
class SpecificFlow():
    def __init__(self):
        self.rfs=0
        self.actions=[] 
        self.postCondition=''
    def addAction(action):
        self.actions.append(action)
class BoundedFlow():
    def __init__(self):
        self.rfs=[]
        self.actions=[]
        self.postCondition='' 
    def addRFS(num):
        self.rfs.append(num)
    def addAction(action):
        self.actions.append(action)
class GlobalFlow():
    def __init__(self):
        self.condition=[]
        self.actions=[] 
        self.postCondition=''
    def addAction(action):
        self.actions.append(action)
