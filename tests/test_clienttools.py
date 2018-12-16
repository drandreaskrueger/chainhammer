#!/usr/bin/env python3
"""
@summary: testing clienttools.py

@version: v42 (4/December/2018)
@since:   30/November/2018
@organization: 
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates
"""

import os
import web3

from hammer.clienttools import *
from hammer.config import RPCaddress

def test_printVersions():
    # if any of the dependencies is NOT installed, this would throw:
    printVersions()

"""
# There is no way of closing the connection again?
# see my question https://github.com/ethereum/web3.py/issues/1152
# So ... no tests for this:

def test_start_web3connection_internal():
    w3=start_web3connection()
    assert (type(w3) == web3.main.Web3)
    w3.close()

def test_start_web3connection_external():
    print (RPCaddress)
    w3=start_web3connection(RPCaddress=RPCaddress)
    assert (type(w3) == web3.main.Web3)

# that means that I can run that start_web3connection only once, 
# and thus it has to become a global object? 
"""

# web3 connection and nodetype
answer = web3connection(RPCaddress=RPCaddress)
w3, chainInfos  = answer
global NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID
NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID = chainInfos


# at least I can test whether it is the correct type:

def test_web3connection():
    assert (type(w3) == web3.main.Web3)


def test_if_poa_then_bugfix_HowtoTestThisNoIdea():
    # nope, cannot run this twice, and already run in web3connection() above
    # if_poa_then_bugfix(w3, NODENAME, CHAINNAME, CONSENSUS)
    assert True
    

def test_getBlockTransactionCount():
    txcount=getBlockTransactionCount(w3, 0)
    assert (txcount >= 0)


def test_unlockAccount():
    # path for the password file
    # unfortunately path if different depending on how py.test is called
    path=os.path.abspath(os.curdir)
    if os.path.split(path)[-1]=="tests":
        os.chdir("..") 
        
    answer = unlockAccount()
    print ("unlock answer:", answer)
    assert answer
    
  
    
    
    