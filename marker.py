import os
import re
import sys
from custom_enum import RegexHandler
from abc import *

class AbstractMarker(metaclass = ABCMeta) :
    @abstractmethod
    def mark(self) :
        pass

class Marker(AbstractMarker) :
    def __init__(self, root) :
        self.root = root
        self.image_files = self.collect_fileinfo(RegexHandler.IMAGE_FILE, root = root)
        pass

    def collect_fileinfo(self, pattern, root) :
        fileinfo = []
        for root, dir, files in os.walk(root) :
            for file in files :
                if RegexHandler.is_pattern_match(file, pattern) :
                    fileinfo.append(FileInfo(name = file, path = root))
        return fileinfo

    def mark(self) :
        '''
        returns a list of image files not linked to markdown text
        '''
        for markdown_info in self.traverse() :
            links = markdown_info.extract_links()
            for link in links :
                if link.is_alive() :
                    self.count(link)
    
    def traverse(self) :
        for root, dir, files in os.walk(self.root) :
            for file in files :
                if RegexHandler.is_pattern_match(file, RegexHandler.MARKDOWN_FILE) :
                    yield MarkdownInfo(name = file, path = root)


    def count(self, image_files, link) :
        link['src']



if __name__ == '__main__' :
    print("Test of Marker starts ")
    if len(sys.argv) == 2 :
        os.chdir(sys.argv[1])
    marker = Marker()
    marker.mark()
