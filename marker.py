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
    def __init__(self, file_tree) :
        self.file_tree = file_tree

    def mark(self) :
        '''
        returns a list of image files not linked to markdown text
        '''
        for md in self.file_tree.traverse() :
            md.extract()



if __name__ == '__main__' :
    print("Test of Marker starts ")
    if len(sys.argv) == 2 :
        os.chdir(sys.argv[1])
    os.chdir("/Users/cjlee/Desktop/workspace/markdown-image-cleaner/sample")
    filetree = FileTree(".")
    filetree.collect()
    marker = Marker(filetree)
    marker.mark()
