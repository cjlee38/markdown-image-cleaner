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
    def __init__(self) :
        pass

    def mark(self) :
        '''
        returns a list of image files not linked to markdown text
        '''
        markdown_files = self.collect_fileinfo(RegexHandler.MARKDOWN_FILE)
        image_files = self.collect_fileinfo(RegexHandler.IMAGE_FILE)
        print(image_files)

        for md in markdown_files :
            links = self.extract_image_links(md)
            for link in links :
                self.is_alive(md, link) # todo : migrate to health checker
            

    def collect_fileinfo(self, pattern) :
        fileinfo = []
        for root, dir, files in os.walk(".") :
            for file in files :
                if RegexHandler.is_pattern_match(file, pattern) :
                    fileinfo.append({
                        'directory' : root,
                        'filename' : file
                    })
        return fileinfo
        

    def extract_image_links(self, fileinfo) :
        def parse_link(sentence) :
            split = RegexHandler.IMAGE_LINK.findall(sentence)[0]
            ret = {
                'alt' : split[0], 
                'src' : split[1]
            }
            return ret

        fp = open(fileinfo['directory'] + '/' + fileinfo['filename'], 'r')
        links = []
        while True :
            sentence = fp.readline()
            if not sentence : break
            if RegexHandler.is_pattern_match(sentence, RegexHandler.IMAGE_LINK) :
                links.append(parse_link(sentence))
        fp.close()
        return links

    def is_alive(self, md, link) :
        image = md['directory'] + '/' + link['src']
        # print(image)
        return os.path.isfile(image)
        # print(os.path.isfile(image))
        # print('md = ', md)
        # print('link = ', link)

if __name__ == '__main__' :
    print("Test of Marker starts ")
    if len(sys.argv) == 2 :
        os.chdir(sys.argv[1])
    marker = Marker()
    marker.mark()
