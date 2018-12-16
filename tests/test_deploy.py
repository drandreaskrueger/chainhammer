#!/usr/bin/env python3
"""
@summary: testing deploy.py

@version: v42 (4/December/2018)
@since:   1/December/2018
@organization: 
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates
"""

import os, timeit
from pprint import pprint
import web3

# web3 connection and nodetype
from hammer.config import RPCaddress, FILE_CONTRACT_SOURCE, ABI
from hammer.clienttools import web3connection
answer = web3connection(RPCaddress=RPCaddress)
global w3, NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID 
w3, chainInfos  = answer
NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID = chainInfos

import hammer.deploy as deploy
import hammer.clienttools as clienttools 
deploy.w3 = w3

# current path one up?
# unfortunately path if different depending on how py.test is called
path=os.path.abspath(os.curdir)
if os.path.split(path)[-1]=="tests":
    os.chdir("..") 


def test_compileContract():
    solfile = os.path.join("hammer", FILE_CONTRACT_SOURCE)
    name, interface = deploy.compileContract(solfile)
    assert name == "simplestorage"
    pprint (interface)
    assert "abi" in interface
    assert "bin" in interface
    

def assertThatAddress(address):
    "trick to check whether well formatted address --> does it have a balance?"
    balance = w3.eth.getBalance(address)
    print(balance)
    assert balance >= 0

    
def test_deployContract():
    solfile = os.path.join("hammer", FILE_CONTRACT_SOURCE)
    name, interface = deploy.compileContract(solfile)
    print ("unlock: ", clienttools.unlockAccount())
    address = deploy.deployContract(interface, ifPrint=True)
    print (address)
    assertThatAddress(address)

    
def test_contractObject_TestedLaterInCombination():
    """
    no need to test this, it is just one web3py call
    
    also, it is tested later in test_trySmartContractMethods() below (*)
    """
    # deploy.contractObject(contractAddress, abi)
    pass


def test_saveTo_and_loadFromDisk():
    
    try: # try to preserve the original file content, if it exists:
        address, abi = deploy.loadFromDisk()
    except FileNotFoundError: # otherwise use dummy data
        address = "0x95368440Aa0b1E90201942085e03eEccDb3dB3E1"
        abi = ABI
    
    answer = deploy.saveToDisk(address, abi)
    assert answer == None
    
    address2, abi2 = deploy.loadFromDisk()
    assert address == address2
    assert abi == abi2  


def test_contract_CompileDeploySave():
    solfile = os.path.join("hammer", FILE_CONTRACT_SOURCE)
    answer = deploy.contract_CompileDeploySave(solfile)
    contractName, contract_interface, contractAddress = answer
    assert contractName == "simplestorage"
    assert "abi" in contract_interface
    assert "bin" in contract_interface
    assertThatAddress(contractAddress)


def test_trySmartContractMethods():
    solfile = os.path.join("hammer", FILE_CONTRACT_SOURCE)
    answer = deploy.contract_CompileDeploySave(solfile)
    _, interface, address = answer
    print ("new contract deployed") # I could have loaded but then test wouldn't be isolated
    
    contract = deploy.contractObject(address, interface["abi"]) # (*) see above
    
    answer1, tx_receipt, answer2 = deploy.trySmartContractMethods(contract)
    
    pprint (dict(tx_receipt))
    assert tx_receipt["gasUsed"] > 0
    assert tx_receipt["blockNumber"] >= 0 

    assert answer1 == answer2 - 1    
    