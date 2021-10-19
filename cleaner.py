from abc import *
import utils
from utils import loud
import os
import shutil

class AbstractCleaner(metaclass = ABCMeta) :
    
    @abstractmethod
    def clean(self, marked):
        pass
    
class Sweeper(AbstractCleaner) :
    '''
    delete actual files
    '''
    def __init__(self) :
        pass
    def clean(self, marked) :
        pass

class Collector(AbstractCleaner) :
    '''
    Dangles are gonna commented out
    Leaks gonna move to 'leaks' folder which is located you run this file
    '''
    MSG = "This line commented out by Markdown-Image-Cleaner"
    LEAKS_FOLDER = "MIC_LEAKS"
    DANGLES_FOLDER = "MIC_DANGLES_BACKUP"

    def clean(self, marked) :
        self.comment(marked['dangles'])
        self.throwaway(marked['leaks'])

    def throwaway(self, leaks: list) -> None :
        leaks_tosave = self.create_folder(Collector.LEAKS_FOLDER)
        for leak in leaks :
            filename = utils.get_filename(leak)
            shutil.move(leak, leaks_tosave + os.sep + filename)
    
    def comment(self, dangles) :
        tosave = self.create_folder(Collector.DANGLES_FOLDER) # backup folder
        for dangle in dangles.keys() : # key = file, value = {index : linkstr}
            backup = self.backup_dangle(dangle, tosave)
            self._comment(backup, dangle, dangles[dangle])

    def create_folder(self, name: str) -> str :
        if name in os.listdir() :
            return self.create_folder(name + "_")
        os.mkdir(name)
        return name

    def backup_dangle(self, pathfile: str, tosave: str) -> str:
        path = utils.get_path(pathfile) # 
        filename = utils.get_filename(pathfile) # name of file to save
        
        os.makedirs(tosave + "/" + path, exist_ok = True)
        save = tosave + "/" + path + "/" + filename

        shutil.copy(pathfile, save) # src, dest
        return save

    def _comment(self, src: str, dest: str, dangle: dict) -> None:
        index = 0
        srcfile = open(src, 'r', encoding = 'UTF-8')
        destfile = open(dest, 'w', encoding = 'UTF-8')
        while read := srcfile.readline() :
            if index in dangle.keys() :
                read = self.wrap(read)
            destfile.write(read)
            index += 1
        srcfile.close()
        destfile.close()

    def wrap(self, read: str) -> str :
        return f"<!--\n{Collector.MSG}\n{read}-->"

class Displayer(AbstractCleaner) :
    '''
    just show file as tree
    '''

    def clean(self, marked) :
        self.display(marked)

    def display(self, marked) :
        dangles = marked['dangles']
        leaks = marked['leaks']
        print (" ======= leaks ======= ")
        for leak in leaks :
            print(leak)
        print (" ======= dangles ======= ")
        for dangle in dangles :
            print(dangle)
            for index in dangles[dangle] :
                print("\t", index, "=>\t", dangles[dangle][index][:-1]) # -1 to delete \n
