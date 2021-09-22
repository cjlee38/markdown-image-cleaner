from custom_enum import RegexHandler
import os
from abc import *

class Component(ABC) :

    def __init__(self, name) :
        self._parent = None
        self._name = name
    
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

    def print(self, depth) :
        tab = " -- " * depth
        parent = self._parent._name if depth != 0 else ''
        print(tab, self._name + '({})'.format(parent))
        if isinstance(self, Directory) :
            for child in self._children :
                child.print(depth + 1)

       
class Directory(Component) :

    def __init__(self, name) :
        super().__init__(name)
        self._children = []
    
    def add(self, component) :
        self._children.append(component)
        component.parent = self
            
    def get(self, name) :
        for child in self._children :
            if child._name == name :
                return child
        return None

    def remove(self, component) :
        self._children.remove(component)
        component.parent = None
    
    def operation(self) :
        results = []
        for child in self._children :
            results.append(child)
        return results

class File(Component) :

    def __init__(self, name) :
        super().__init__(name)

    def operation(self) :
        return "Leaf"

class MarkdownFile(File) :
    def __init__(self, name) :
        super().__init__(name)
        self.links = {}
    
    def extract_links(self) :
        self.links['image'] = self.extract_image_links()
        self.links['url'] = self.extract_url_links()
        return self.links

    def get_links(self) :
        return self.links

    def extract_image_links(self, fileinfo) :
        pass

    def is_alive(self, md, link) :
        pass

class ImageFile(File) :
    def __init__(self, name) :
        super().__init__(name)
        self.count = 0
    
    def decrease(self) :
        self.count -= 1
        return self.count

    def get_count(self) :
        return self.count

class FileTree :
    
    def __init__(self, root) :
        self._root = root
        self._tree = None
    
    def collect(self) :
        self._tree = Directory(self._root)
        for parent, dirs, files in os.walk(self._root) :
            p = self.find(self._tree, parent)
            for dir in dirs :
                p.add(Directory(dir))
            for file in files :
                if RegexHandler.is_pattern_match(file, RegexHandler.MARKDOWN_FILE) :
                    p.add(MarkdownFile(file))
                if RegexHandler.is_pattern_match(file, RegexHandler.IMAGE_FILE) :
                    p.add(ImageFile(file))
    
    def find(self, parent: Component, route: str) -> Component:
        if parent._name == route :
            return parent
        p = parent
        for r in route.split("/")[1:] :
            p = p.get(r)
        return p
    
    def print(self) :
        self._tree.print(0)

if __name__ == '__main__' :
    print("file test code starts")
    # os.path.isabs()
    os.chdir("/Users/cjlee/Desktop/workspace/markdown-image-cleaner")
    f = FileTree(".")
    f.collect()
    f.print()
    
