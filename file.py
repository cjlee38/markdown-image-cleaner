from abc import *

class FileInfo(metaclass = ABCMeta) :
    def __init__(self, name, path) :
        self.name = name
        self.abs_path, self.rel_path = parse_path(path)

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