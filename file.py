from custom_enum import RegexHandler
import os
from abc import *
import utils

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
    '''
    It describe directories and files using Composite-pattern
    currently just store directories and image-files(png, jpg, etc ...)
    '''
    def __init__(self) :
        self._root = None
        self._tree = None
        self._image_count = 0
    
    def build(self, root: str, ignores: list) -> None:
        self._root = root
        self._tree = Directory(self._root, self._root)
        for parent, dirs, files in os.walk(self._root) :
            dirs[:] = utils.exclude_ignores(parent, dirs, ignores) # [:] needed to modifies in-place
            p = self.find(parent)
            for dir in dirs :
                p.add(Directory(dir, parent))
            for file in files :
                if RegexHandler.is_pattern_match(file, RegexHandler.IMAGE_FILE) :
                    p.add(ImageFile(file, parent))
                    self._image_count += 1
    
    def find(self, path: str) -> Component:
        p = self._tree
        if p._name == path :
            return p
        start = os.path.relpath(path, self._root)
        for r in start.split(os.sep) :
            if not p :
                return None
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

    def is_alive(self, pathfile: str) -> bool :
        p = self.find(pathfile)
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

