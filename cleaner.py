from abc import *

class AbstractCleaner(metaclass = ABCMeta) :
    
    def __init__(self, deadlinks, unlinks) :
        self._deadlinks = deadlinks
        self._unlinks = unlinks
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
    def __init__(self, deadlinks, unlinks) :
        super().__init__(deadlinks, unlinks)

    def clean(self) :
        print(deadlinks)
        print("----")
        print(unlinks)
