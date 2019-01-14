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

INFO_EXAMPLE={'diagrams': {'blocktimestampsTpsAv': 162.36666666666667,
              'filename': 'img/TEMP-20190114-1519_blks10-40.png',
              'prefix': 'TEMP'},
 'node': {'chain_id': 326432352,
          'chain_name': '???',
          'consensus': 'clique',
          'name': 'Geth',
          'network_id': 500,
          'rpc_address': 'http://localhost:8545',
          'type': 'Geth',
          'version': 'v1.8.14-stable-316fc7ec',
          'web3.version.node': 'Geth/v1.8.14-stable-316fc7ec/linux-amd64/go1.10.3'},
 'send': {'block_first': 10,
          'block_last': 40,
          'empty_blocks': 10,
          'num_txs': 10000,
          'sample_txs_successful': True},
 'tps': {'finalTpsAv': 156.10037659498764,
         'peakTpsAv': 160.8096672375769,
         'start_epochtime': 1547475588.1457317},
 'ATTENTION' : "not real, file created by unittests!"}

def dummy_infofile():
    data = INFO_EXAMPLE
    with open(FILE_LAST_EXPERIMENT, "w") as f:
        json.dump(data, f)


def test_readInfofile():
    # so that the file exists:
    dummy_infofile()
    data = mg.read_infofile(FILE_LAST_EXPERIMENT)
    assert data['send']['num_txs'] == 10000
    
    
def test_format_infofile_content():
    T = mg.format_infofile_content(INFO_EXAMPLE)
    assert type(T) == type (" ")
    
    
def test_readTpsLog():
    mg.readTpsLog(fn=FILE_LAST_EXPERIMENT) # N.B.: Wrong file, but doesn't matter.
    
    
def test_title():
    T=mg.title(INFO_EXAMPLE)
    assert T=="Geth v1.8.14-stable-316fc7ec with 10000 txs: 162.4 TPS"
    
    
def test_save_page():
    answer = mg.save_page("hello world", "testing.txt", folder=".")
    os.remove(answer)
    assert answer=="./testing.txt"
    
    
def test_timestamp_humanreadable():
    answer = mg.timestamp_humanreadable(0)
    # in my case the full answer is:     19700101-0100 = why 01:00 am ?
    # --> only check beginning because local timezones:
    assert answer[0:2] == "19" 
    

def test_filename():
    assert mg.filename(INFO_EXAMPLE) == "Geth_20190114-1519_txs10000"
    
    
def test_createElements():
    answers = mg.createElements(INFO_EXAMPLE, FILE_LAST_EXPERIMENT) # N.B.: Wrong file, but doesn't matter.
    assert answers[3] == "img/TEMP-20190114-1519_blks10-40.png"
    
    
def test_makeAndSave_MarkdownPage():
    answer = mg.makeAndSave_MarkdownPage(INFO_EXAMPLE, "title", "info", 
                                         "tpslog", "image_location",
                                         runs_folder=".")
    os.remove(answer)
    assert answer == "./Geth_20190114-1519_txs10000.md"


def test_makeAndSave_HTMLPage():
    answer = mg.makeAndSave_HTMLPage(INFO_EXAMPLE, "title", "info", 
                                         "tpslog", "image_location",
                                         runs_folder=".")
    os.remove(answer)
    assert answer == "./Geth_20190114-1519_txs10000.html"


def test_CLI_params():
    try:
        mg.CLI_params()
    except SystemExit:
        pass
    