#!/usr/bin/env python3
"""
@summary: testing send.py

@version: v42 (4/December/2018)
@since:   1/December/2018
@organization: 
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates
"""

import os
from pprint import pprint
from web3.utils import datatypes

# web3 connection and nodetype
from hammer.config import RPCaddress, FILE_CONTRACT_SOURCE
from hammer.clienttools import web3connection
answer = web3connection(RPCaddress=RPCaddress)
global w3, NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID 
w3, chainInfos  = answer
NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID = chainInfos

import hammer.send as send
import hammer.deploy as deploy
deploy.w3 = send.w3 = w3

# current path one up?
# unfortunately path if different depending on how py.test is called
path=os.path.abspath(os.curdir)
if os.path.split(path)[-1]=="tests":
    os.chdir("..") 
   

# fixture: create a contract that every test here can be using
solfile = os.path.join("hammer", FILE_CONTRACT_SOURCE)
_,interface,address = deploy.contract_CompileDeploySave(solfile)
contract = deploy.contractObject(address, interface["abi"])
abi = interface["abi"]
 

def test_initialize_fromAddress():
    contract = send.initialize_fromAddress()
    print (contract)
    assert ("%s" % contract).startswith("<web3.utils.datatypes.Contract object")


def test_contract_set_via_web3():
    arg = 1000
    stored = send.try_contract_set_via_web3(contract, arg)
    assert arg == stored 


def test_contract_method_ID():
    methodname = "get"
    answer = send.contract_method_ID(methodname, abi)
    print (answer)
    assert answer == "0x6d4ce63c"


def test_argument_encoding():
    method_ID = send.contract_method_ID("set", abi) # TODO: make this "set" flexible for any method name
    data = send.argument_encoding(method_ID, arg=42)
    print (data)
    assert data == "0x60fe47b1000000000000000000000000000000000000000000000000000000000000002a"
    
    
def test_contract_set_via_RPC():
    arg = 1001
    tx = send.contract_set_via_RPC(contract, arg=arg)
    print (tx)
    assert tx.startswith("0x")
    tx_receipt = w3.eth.waitForTransactionReceipt(tx)
    stored = contract.functions.get().call()
    assert arg == stored


def test_many_transactions_consecutive():
    numTx=10
    txs = send.many_transactions_consecutive(contract, numTx)
    print (txs)
    assert len(txs)==numTx
    assert txs[0].startswith("0x")
    assert txs[numTx-1].startswith("0x")


def test_many_transactions_threaded():
    answer = send.many_transactions_threaded(contract, numTx=10)
    assert answer == None 
    # there are no return values, so what can be tested is 
    # that it does not throw an exception


def test_many_transactions_threaded():
    answer = send.many_transactions_threaded_Queue(contract, numTx=10, num_worker_threads=3)
    assert answer == None 
    # there are no return values, so what can be tested is 
    # that it does not throw an exception

    
def test_many_transactions_threaded_in_batches():
    answer = send.many_transactions_threaded_in_batches(contract, numTx=10, batchSize=3)
    assert answer == None 
    # there are no return values, so what can be tested is 
    # that it does not throw an exception


def test_sendmany_HowtoTestThisNoIdea():
    # answer = send.sendmany()
    # how to test this? Please make suggestions
    pass
  


