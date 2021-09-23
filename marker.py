import os
import re
import sys
from custom_enum import RegexHandler, ContentType
from web import Requester
from abc import *
from file import *

class AbstractMarker(metaclass = ABCMeta) :
    @abstractmethod
    def mark(self) :
        pass

class Marker(AbstractMarker) :
    def __init__(self, file_tree) :
        self._file_tree = file_tree

    def mark(self) :
        deads = []
        for pathfile in self.traverse() :
            deads.extend(self.checkoff(pathfile))
        unlinked = self._file_tree.get_garbages()
        return deads, unlinked

    def traverse(self) :
        for parent, dirs, files in os.walk(self._file_tree.get_root()) :
            for file in files :
                if RegexHandler.is_pattern_match(file, RegexHandler.MARKDOWN_FILE) :
                    yield "/".join([parent, file])

    def checkoff(self, pathfile) :
        deads = []
        with open(pathfile, 'r', encoding = 'UTF-8') as f :
            for line in f.readlines() :
                search = RegexHandler.IMAGE_LINK.search(line)
                if search :
                    link = search.group(2)
                    if link.startswith('http') :
                        if not Requester.is_alive(link) :
                            deads.append(link)
                    elif not self._file_tree.count(link) : # link url
                        deads.append(link)
        return deads




if __name__ == '__main__' :
    print("  Test of Marker starts  ")
    if len(sys.argv) == 2 :
        os.chdir(sys.argv[1])
    filetree = FileTree(".")
    filetree.build()
    marker = Marker(filetree)
    res = marker.mark()
    print(res[0])
    for i in res[1] :
        print(i)

