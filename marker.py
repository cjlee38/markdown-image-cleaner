import os
import re
import sys
from custom_enum import RegexHandler, ContentType
from abc import *
from file import *

class AbstractMarker(metaclass = ABCMeta) :
    @abstractmethod
    def mark(self) :
        pass

class Marker(AbstractMarker) :
    def __init__(self, root) :
        self.root = root
        self.file_tree = None

    def mark(self) :
        '''
        returns a list of image files not linked to markdown text
        '''
        



if __name__ == '__main__' :
    print("Test of Marker starts ")
    if len(sys.argv) == 2 :
        os.chdir(sys.argv[1])
    os.chdir("/Users/cjlee/Desktop/workspace/markdown-image-cleaner/sample")
    marker = Marker(".")
    marker.mark()
    marker.file_struct.print()
