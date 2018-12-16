#!/usr/bin/env python3
"""
@summary: testing clienttype.py

@version: v42 (4/December/2018)
@since:   30/November/2018
@organization: 
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates
"""

import pytest
import web3
from hammer.clienttype import *
from hammer.config import RPCaddress

global w3
w3=simple_web3connection(RPCaddress)


def test_simple_web3connection():
    global w3
    assert type(w3) == web3.main.Web3

    
def test_curl_post():
    method="eth_blockNumber"
    answer = curl_post(method, ifPrint=True)
    print (method, answer)
    assert type(answer)==type("") # that the answer (blocknumber) is a string


def test_curl_post_MethodNotExistentError():
    method="eth_thisMethodDoesNotExist"
    with pytest.raises(MethodNotExistentError):
        answer = curl_post(method, ifPrint=True)
        print (answer)


def test_clientType():
    answer = clientType(w3)
    print (answer)
    assert len(answer) == 6
    
    