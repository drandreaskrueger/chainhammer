#!/usr/bin/env python3
"""
@summary: testing markdown_generator.py

@version: v50 (13/January/2019)
@since:   13/January/2019
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates
"""


################################################################################
# current path one up?
# path is different depending on how py.test is called, so correct this here:
path=os.path.abspath(os.curdir)
if os.path.split(path)[-1]=="tests":
    os.chdir("..") 

################################################################################

