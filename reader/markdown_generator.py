#!/usr/bin/env python3
"""
@summary:  human-readable page after each experiment
            incl tps.py outputs
            incl diagrams
            incl (e.g. network) start parameters

@version: v50 (13/January/2019)
@since:   13/January/2019
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates
"""

################################################################################
## Dependencies:

# standard library:
import sys, os, json
from pprint import pprint

# pypi:

# chainhammer
# extend sys.path for imports:
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from hammer.config import FILE_LAST_EXPERIMENT

################################################################################

def read_infofile(fn=FILE_LAST_EXPERIMENT):
    with open(fn, "r") as f:
        data = json.load(f)
    return data


def CLI_params():
    if len(sys.argv)!=2:
        print ("Please give one argument, the filename of the experiment-infofile.")
        exit()
    if len(sys.argv)==2:
        INFOFILE=sys.argv[1]
        print ("Reading from INFOFILE ", INFOFILE)
    return INFOFILE


if __name__ == '__main__':
    INFOFILE = CLI_params()
    data = read_infofile(INFOFILE)
    pprint (data)
    print ()
    
        