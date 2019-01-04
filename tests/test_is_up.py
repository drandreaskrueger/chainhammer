#!/usr/bin/env python3
"""
@summary: testing is_up.py

@version: v47 (04/January/2019)
@since:   04/January/2019
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates
"""

# standard library
import os

# chainhammer:
from hammer.config import RPCaddress
import hammer.is_up as is_up

# tests:

def test_call_port__CORRECT__():
    assert is_up.call_port() == (True, None)

def test_call_port__INCORRECT__():
    assert is_up.call_port("http://loKalhost:0") == (False, 'ConnectionError')
    
def test_simple_RPC_call__CORRECT__():
    assert is_up.simple_RPC_call() == (True, None)
    
def test_simple_RPC_call__INCORRECT__():
    assert is_up.simple_RPC_call(method="dummy_wrong") == (False, 'MethodNotExistentError')

def test_loop_until_is_up():
    assert is_up.loop_until_is_up(timeout=3)
    