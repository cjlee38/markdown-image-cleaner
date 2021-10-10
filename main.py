from marker import Marker
from cleaner import *
from custom_enum import *
from file import *
from utils import loud
import sys
import argparse

def config() :
    clean_type = set_clean_type()

def set_clean_type() :
    if len(sys.argv) == 1 :
        clean_type = CleanType.SWEEP


'''
# Todo
ignore folder or file settings
'''
if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description = 'markdown-image-cleaner')
    parser.add_argument('--clean-type', '-c', 
                        type = str,
                        default = "display",
                        choices = ["display", "collect", "sweep"],
                        help = "Determine type to clean. \
                            Options are display, collect, sweep. \
                            Default value is display")
    parser.add_argument('--directory', '-d',
                        type = str,
                        default = ".",
                        help = "Change to direcotry if specified. \
                            Default is current directory(.)")
    args = parser.parse_args()
    if len(sys.argv) == 1 :
        loud("There is no arguments.")
        loud("You can print usage by command 'python main.py -h'")
    root = args.directory
    cleantype = args.clean_type
    
    filetree = FileTree()
    filetree.build(root)

    marker = Marker()
    marked = marker.mark(filetree)
    
    cleaners = {
        'display' : Displayer(),
        'collect' : Collector(),
        'sweep' : Sweeper()
    }
    cleaner = cleaners.get(cleantype)
    cleaner.clean(marked)
