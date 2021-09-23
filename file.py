import os
from abc import *

class FileInfo(metaclass = ABCMeta) :
    def __init__(self, name, path) :
        self.name = name
        self.abs_path, self.rel_path = self.parse_path(path)

    def parse_path(self, path) :
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

    def operation(self) :
        return "Leaf"

class MarkdownFile(File) :
    def __init__(self, name, path) :
        super().__init__(name, path)
        self._links = {}
    
    def extract(self) :
        # with open(self._path + "/" + self._name, 'r', encoding = 'UTF-8') as f :
        #     for line in f.readlines() :
        #         if RegexHandler.is_pattern_match(RegexHandler.IMAGE_LINK) :
        #             self._links.
        # self.links['image'] = self.extract_image_links()
        # self.links['url'] = self.extract_url_links()
        return self._links

    def get_links(self) :
        return self._links

    def extract(self, fileinfo) :
        pass

class ImageInfo(FileInfo) :
    def __init__(self, name, path) :
        super().__init__(name, path)
        self._count = 0
    
    def increase(self) :
        self._count += 1
        return self._count

    def get_count(self) :
        return self._count

class FileTree :
    
    def __init__(self, root) :
        self._root = root
        self._tree = None
    
    def build(self) :
        self._tree = Directory(self._root, ".")
        for parent, dirs, files in os.walk(self._root) :
            p = self.find(parent)
            for dir in dirs :
                p.add(Directory(dir, parent))
            for file in files :
                if RegexHandler.is_pattern_match(file, RegexHandler.IMAGE_FILE) :
                    p.add(ImageFile(file, parent))
    
    def find(self, path: str) -> Component:
        p = self._tree
        if p._name == path :
            return p

        for r in path.split(os.sep) :
            if r == '.' :
                continue
            if r == '..' :
                p = p._parent
            else :
                p = p.get(r)
        return p
    
    def print(self) :
        self._tree.print(0)

    def get_root(self) :
        return self._root
<<<<<<< Updated upstream

    def count(self, pathfile) :
        p = self.find(pathfile)
        if p :
            p.increase()
            return True
        return False

=======

    def count(self, pathfile) :
        p = self.find(pathfile)
        if p :
            p.increase()
            return True
        return False

>>>>>>> Stashed changes
    def get_garbages(self) :
        return self._get_garbages(self._tree)
    
    def _get_garbages(self, parent) :
        for child in parent._children :
            if isinstance(child, Directory) :
                yield from self._get_garbages(child)
            elif isinstance(child, ImageFile) and child._count == 0 :
                yield child._path + "/" + child._name

        

if __name__ == '__main__' :
    print("file test code starts")
    # os.path.isabs()
    os.chdir("../")
    # os.chdir("/Users/cjlee/Desktop/workspace/markdown-image-cleaner")
    f = FileTree(".")
    f.collect()
    f.print()
    
