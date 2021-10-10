from abc import *

class AbstractCleaner(metaclass = ABCMeta) :
    
    def __init__(self, marked) :
        self._marked = marked

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
        
    def clean(self) :
        pass

class Displayer(AbstractCleaner) :
    '''
    just show file as tree
    '''
    # def __init__(self, deadlinks, unlinks) :
    #     super().__init__(deadlinks, unlinks)

    def clean(self) :
        self.display()

    def display(self) :
        dangles = self._marked['dangles']
        leaks = self._marked['leaks']
        print (" ======= leaks ======= ")
        for leak in leaks :
            print(leak)
        print (" ======= dangles ======= ")
        for dangle in dangles :
            print(dangle)
            for file in self._marked['dangles'][dangle] :
                print("\t", file)

if __name__ == '__main__' :
    import os
    import sys
    from file import FileTree
    from marker import Marker
    print("  Test of Cleaner starts  ")
    if len(sys.argv) == 2 :
        os.chdir(sys.argv[1])
    filetree = FileTree(".")
    filetree.build()
    marker = Marker(filetree)
    res = marker.mark()
    displayer = Displayer(res)
    displayer.clean()
