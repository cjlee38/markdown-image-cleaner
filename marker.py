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
        marked = {
            'dangles' : {},
            'leaks' : []
        }
        for parent, file in self.traverse() :
            check = self.checkoff(parent, file)
            if check :
                pathfile = os.path.normpath(parent + "/" + file)
                marked['dangles'][pathfile] = check
        marked['leaks'] = list(self._file_tree.get_garbages())
        return marked

    def traverse(self) -> tuple :
        for parent, dirs, files in os.walk(self._file_tree.get_root()) :
            for file in files :
                if RegexHandler.is_pattern_match(file, RegexHandler.MARKDOWN_FILE) :
                    yield parent, file

    def checkoff(self, parent: str, file: str) :
        '''
        collect dead links while reading each line.
        '''
        deadlinks = {}
        pathfile = "/".join([parent, file])
        with open(pathfile, 'r', encoding = 'UTF-8') as f :
            for idx, line in enumerate(f.readlines()) :
                image_link = self.is_image_link(line, parent)
                if image_link and not self.pulse(image_link):
                    deadlinks[idx] = line
        return deadlinks

    def is_image_link(self, line: str, parent: str) -> str :
        '''
        Check if readline has image_link and that link is alive.
        If It matches to IMAGE_LINK(regex) and dead, then return False.
        '''
        search = RegexHandler.IMAGE_LINK.search(line)
        if search :
            return self.rebuild_link(parent, search.group(2))
        return None

    def rebuild_link(self, parent: str, image_link: str) :
        '''
        match image_link path to real path
        '''
        if image_link.startswith("/") or image_link.startswith("http"):
            return image_link
        return os.path.normpath("/".join([parent, image_link]))
            
    def pulse(self, link: str) -> bool:
        '''
        Heart beat to image_file.
        If it is a kind of file, FileTree gonna check if it's alive.
        Or a kind of http, Requester gonna check.
        '''
        if link.startswith('http') :
            return Requester.is_alive(link)
        return self._file_tree.is_alive(link)

if __name__ == '__main__' :
    print("  Test of Marker starts  ")
    if len(sys.argv) == 2 :
        os.chdir(sys.argv[1])
    filetree = FileTree(".")
    filetree.build()
    # filetree.print()
    marker = Marker(filetree)
    res = marker.mark()
    from pprint import pprint
    pprint(res)

