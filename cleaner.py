from abc import *

class Cleaner(metaclass = ABCMeta) :
    
    @abstractmethod
    def clean(self):
        pass
    
class Sweeper(Cleaner) :
    '''
    delete actual files
    '''
    def __init__(self) :
        pass
    def clean(self) :
        pass
