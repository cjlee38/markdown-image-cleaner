from marker import Marker
from cleaner import *
from custom_enum import *
from file import *
from utils import loud, exists
from argument import ArgParser

import sys
import yaml



'''
# Todo
ignore folder or file settings
'''

def validate(args) :
    if len(sys.argv) == 1 :
        loud("There is no arguments.")
        loud("You can print usage by command 'python main.py -h'")

    exists(args['directory'])
    for i in args['ignore_image'] :
        exists(i)
    for i in args['ignore_markdown'] :
        exists(i)

def warning(args) :
    if args['clean_type'] == 'sweep' :
        loud("You chose 'sweep' as clean type. \
            This action is irreversible. \
            If want to continue, input 'Y/y'")
        YN = input()
        if YN.lower() != 'y' :
            raise Exception("Halted by user.")
            
def load_configfile() :
    CONFIG_FILE = "config.yaml"
    with open(CONFIG_FILE, 'r', encoding = 'UTF-8') as f :
        configs = yaml.load(f, Loader = yaml.FullLoader)
    return configs

if __name__ == "__main__" :
    '''
    # todo
    show summary
    "/".join -> os.sep.join(as function)
    '''
    
    configs = load_configfile()
    parser = ArgParser()
    args = parser.parse(configs)
    validate(args)
    warning(args)

    
    filetree = FileTree()
    filetree.build(args['directory'], args['ignore_image'])

    marker = Marker()
    marked = marker.mark(filetree, args['ignore_markdown'])
    
    cleaners = {
        'display' : Displayer(),
        'collect' : Collector(),
        'sweep' : Sweeper()
    }
    cleaner = cleaners.get(args['clean_type'])
    cleaner.clean(marked)
    
    summary = marker.summary(marked)
    summary
    # loud(summary)

