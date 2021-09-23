import os
import re
import sys
from custom_enum import RegexHandler, ContentType
from web import Requester
from abc import *
from file import *

class AbstractMarker(ABC) :
    @abstractmethod
    def mark(self) :
        pass

class Marker(AbstractMarker) :
    def __init__(self, file_tree) :
        self._file_tree = file_tree

    def mark(self) :
        deadlinks = [self.checkoff(pathfile) for pathfile in self.traverse()]
        unlinked = list(self._file_tree.get_garbages())
        return deadlinks, unlinked

    def traverse(self) :
        for parent, dirs, files in os.walk(self._file_tree.get_root()) :
            for file in files :
                if RegexHandler.is_pattern_match(file, RegexHandler.MARKDOWN_FILE) :
                    yield "/".join([parent, file])

    def checkoff(self, pathfile) :
        deadlinks = []
        with open(pathfile, 'r', encoding = 'UTF-8') as f :
            for idx, line in enumerate(f.readlines()) :
                if not self.inspect(line) :
                    deadlinks.append(DeadLink(idx, line, pathfile))
        return deadlinks

    def inspect(self, line) -> None :
        search = RegexHandler.IMAGE_LINK.search(line)
        if search and not self.pulse(search.group(2)) :
            return False
        return True
            
    def pulse(self, link) :
        if link.startswith('http') :
            return Requester.is_alive(link)
        return self._file_tree.is_alive(link)

class DeadLink :
    def __init__(self, idx, string, md) :
        self._idx = idx
        self._link =  RegexHandler.IMAGE_LINK.search(string).group(2)
        self._md = md
    
    def __repr__(self) :
        return self._md + "(" + self._link + ")"


if __name__ == '__main__' :
    print("  Test of Marker starts  ")
    if len(sys.argv) == 2 :
        os.chdir(sys.argv[1])
    filetree = FileTree(".")
    filetree.build()
    marker = Marker(filetree)
    res = marker.mark()
    print(res[0])
    print(res[1])

