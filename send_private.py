#!/usr/bin/env python3
# from __future__ import print_function

"""
@summary: submit to private contract .set(arg) transactions with privateFor field

@version: v06 (24/April/2018)
@since:   24/April/2018
@author:  https://github.com/drandreaskrueger
"""

RPCaddress='http://localhost:22000' # 22000 = node 1 of the 7nodes quorum example
PRIVATE_FOR = ["ROAZBWtSacxXQrOe3FGAqJDyJjFePR5ce4TSIzmJ0Bc="]
ABI = [{"constant":True,"inputs":[],"name":"storedData","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"x","type":"uint256"}],"name":"set","outputs":[],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"get","outputs":[{"name":"retVal","type":"uint256"}],"payable":False,"type":"function"},{"inputs":[{"name":"initVal","type":"uint256"}],"type":"constructor"}];

from web3 import Web3, HTTPProvider # pip3 install web3
from web3.utils.abi import filter_by_name, abi_to_signature
from web3.utils.encoding import pad_hex

import sys, time, random
from threading import Thread
from queue import Queue
from pprint import pprint

import requests # pip3 install requests


def unlockAccount(address=None, password="", duration=3600):
    """
    unlock once, then leave open, to not loose time for unlocking
    """
    if not address:
        address = w3.eth.coinbase
    return w3.personal.unlockAccount(address, password, duration)


def initialize(contractTx_blockNumber=1, contractTx_transactionIndex=0):
    """
    use example contract from 7 nodes example
    if called without arguments, it assumes that the very first transaction was done by
    ./runscript.sh script1.js
    """
    abi = ABI
    
    print ("Getting the address of the example contract that was deployed")
    block = w3.eth.getBlock(contractTx_blockNumber)
    transaction0=block["transactions"][contractTx_transactionIndex]
    print ("transaction hash = ", w3.toHex(transaction0))
    address=w3.eth.getTransactionReceipt(transaction0)["contractAddress"]
    print ("contract address = ", address)
    contract = w3.eth.contract(address=address, abi=abi)
    print (contract)
   
    print("unlock account:", unlockAccount())

    # pprint (dir(contract))
    return contract


def contract_set_via_web3(contract, arg, privateFor=PRIVATE_FOR, gas=90000):
    """
    call the .set(arg) method, possibly with 'privateFor' tx-property
    using the web3 method 
    """
    txParameters = {'from': w3.eth.coinbase,
                    'gas' : gas}
    if privateFor:
        txParameters['privateFor'] = privateFor  # untested
        
    pprint (txParameters)
        
    tx = contract.functions.set( x=arg ).transact(txParameters)
    print ("[sent via web3]", end=" ")
    tx = w3.toHex(tx)
    return tx


def test_contract_set_via_web3(contract):
    """
    test the above
    """
    tx = contract_set_via_web3(contract, arg=888)
    print (tx)
    storedData = contract.functions.get().call()
    print (storedData) 




if __name__ == '__main__':

    global w3
    w3 = Web3(HTTPProvider(RPCaddress, request_kwargs={'timeout': 120}))
    print ("w3.eth.accounts = ", w3.eth.accounts)
    
    contract = initialize()

    test_contract_set_via_web3(contract)

