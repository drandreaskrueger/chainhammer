#!/usr/bin/env python3
"""
@summary: testing markdown_generator.py

@version: v50 (13/January/2019)
@since:   13/January/2019
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates
"""

import os, json
from hammer.config import RPCaddress, FILE_CONTRACT_SOURCE, FILE_LAST_EXPERIMENT
import reader.markdown_generator as mg


################################################################################
# current path one up?
# path is different depending on how py.test is called, so correct this here:
path=os.path.abspath(os.curdir)
if os.path.split(path)[-1]=="tests":
    os.chdir("..") 

################################################################################

def dummy_infofile():
    dummy = "not real, file created by tests/test_send.py"
    data = {"send": {"num_txs" : dummy}}
    with open(FILE_LAST_EXPERIMENT, "w") as f:
        json.dump(data, f)

def test_readInfofile():
    # so that the file exists:
    dummy_infofile()
    mg.read_infofile(FILE_LAST_EXPERIMENT)
    
    
def test_CLI_params():
    try:
        mg.CLI_params()
    except SystemExit:
        pass
    