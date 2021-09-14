from abc import *

class AbstractCleaner(metaclass = ABCMeta) :
    
    @abstractmethod
    def clean(self):
        pass
    
class Sweeper(AbstractCleaner) :
    '''
    delete actual files
    '''
    def __init__(self) :
        pass
    def clean(self) :
        pass

class Collector(AbstractCleaner) :
    '''
    move to trash folder
    '''
    def __init__(self) :
        pass
    def clean(self) :
        pass

class Displayer(AbstractCleaner) :
    '''
    just show file as tree
    '''
    def __init__(self) :
        pass
    def clean(self) :
        pass
    
