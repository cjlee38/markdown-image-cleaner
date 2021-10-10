from custom_enum import RegexHandler
import os
from abc import *

class Component(ABC) :

    def __init__(self, name, path) :
        self._parent = None
        self._path = path
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
        print(tab, self._name + '(parent = {})(path = {})'.format(parent, self._path))
        if isinstance(self, Directory) :
            for child in self._children :
                child.print(depth + 1)
     
class Directory(Component) :

    def __init__(self, name, path) :
        super().__init__(name, path)
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

    def __init__(self, name, path) :
        super().__init__(name, path)

    def operation(self) :
        pass

class ImageFile(File) :
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
    
    def find(self, path: str, debug = False) -> Component:
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

    def is_alive(self, pathfile) :
        p = self.find(pathfile, debug = True)
        if p :
            p.increase()
            return True
        return False

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
    os.chdir("./sample")
    # os.chdir("/Users/cjlee/Desktop/workspace/markdown-image-cleaner")
    f = FileTree(".")
    f.build()
    f.print()
    
