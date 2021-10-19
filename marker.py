import os
import re
import sys
from custom_enum import RegexHandler
from web import Requester
from abc import *
from file import *
from utils import loud

class AbstractMarker(ABC) :
    @abstractmethod
    def mark(self) :
        pass

class Marker(AbstractMarker) :

    def __init__(self) :
        self._file_tree = None
        self._line_count = 0

    def mark(self, file_tree: FileTree, ignores: list) -> dict:
        self._file_tree = file_tree
        marked = { 'dangles' : {}, 'leaks' : [] }
        for parent, file in self.traverse(ignores) :
            check = self.checkoff(parent, file)
            if check :
                pathfile = os.path.normpath(parent + "/" + file)
                marked['dangles'][pathfile] = check
        marked['leaks'] = list(self._file_tree.get_garbages())
        return marked
    
    def summary(self, marked: dict) -> None :
        counts = {
            'leaks' : {'all' : 0, 'fail' : 0 },
            'dangles' : { 'all' : 0, 'fail' : 0 }
        }
        dangle_all = self._line_count
        dangle_fail = sum([len(v) for k, v in marked['dangles'].items()])
        leak_all = self._file_tree._image_count
        leak_fail = len(marked['leaks'])
        
        loud(f"LEAKS\t\t= \t{leak_fail}/{leak_all}({leak_fail * 100/ leak_all}%)")
        loud(f"DANGLES\t= \t{dangle_fail}/{dangle_all}({dangle_fail * 100/ dangle_all}%)")

    def traverse(self, ignores: list) -> tuple :
        for parent, dirs, files in os.walk(self._file_tree.get_root()) :
            dirs[:] = utils.exclude_ignores(parent, dirs, ignores)
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
                if image_link :
                    self._line_count += 1
                    if not self.pulse(image_link):
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
        match image_link path to full absolute path
        '''
        if image_link.startswith("http"):
            return image_link
        prefix = self._file_tree.get_root() if image_link.startswith(os.sep) else parent
        return os.path.normpath("/".join([prefix, image_link]))
            
    def pulse(self, link: str) -> bool:
        '''
        Heart beat to image_file.
        '''
        if link.startswith('http') :
            return Requester.is_alive(link)
        return self._file_tree.is_alive(link)

