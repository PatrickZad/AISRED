class GWT(object):
    __slots__ = ('gwt_id', 'Scenario', 'Features', 'Givens', 'Whens', 'Thens')


class TagedGWT(GWT):
    __slots__ = ('useCaseName', 'BranchScenarios', 'preScenarios', 'postScenarios', 'flowType')


class Sentence(object):
    __slots__ = ('sentence_id', 'type', 'content', 'sequence')


class TagedSentence(Sentence):
    __slots__ = ('secondType', 'associations')


class Association(object):
    __slots__ = ('gwtId', 'sentenceId', 'connect_type')


class Scenario(object):
    __slots__ = ('gwtId', 'conditionIds')


