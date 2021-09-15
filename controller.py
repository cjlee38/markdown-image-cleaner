from marker import Marker
from cleaner import *
from custom_enum import *
import sys


def config() :
    clean_type = set_clean_type()

def set_clean_type() :
    if len(sys.argv) == 1 :
        clean_type = CleanType.SWEEP


'''
# Todo
http requests for check if alive
root directory settings
ignore folder or file settings
'''
if __name__ == "__main__" :
    clean_type = sys.argv[1]
    marker = Marker()
    l = marker.mark()
