import os
from abc import *

class Component(ABC) :

    @property
    def parent(self) :
        return self._parent
    
    @parent.setter
    def parent(self, parent) :
        self._parent = parent
    
    def add(self, component) -> None :
        pass
    
    def remove(self, component) -> None :
        pass

    def is_composite(self) -> bool :
        return False

    @abstractmethod
    def operation(self) :
        pass

class FileInfo(ABC) :
    def __init__(self, name, path) :
        self.name = name
        self.abs_path, self.rel_path = self.parse_path(path)

    def parse_path(self, path) :
        # todo : fix this lol
        pass

    def get_name(self) :
        return self.name
    
    def get_abs_path(self) :
        return self.abs_path

    def get_rel_path(self) :
        return self.rel_path

class MarkdownInfo(FileInfo) :
    def __init__(self, name, path) :
        super().__init__(name, path)
        self.links = {}
    
    def extract_links(self) :
        self.links['image'] = self.extract_image_links()
        self.links['url'] = self.extract_url_links()
        return self.links

    def get_links(self) :
        return self.links

class ImageInfo(FileInfo) :
    def __init__(self, name, path) :
        super().__init__(name, path)
        self.count = 0
    
    def decrease(self) :
        self.count -= 1
        return self.count

    def get_count(self) :
        return self.count


# ------------------ #
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