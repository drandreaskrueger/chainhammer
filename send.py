#!/usr/bin/env python
from __future__ import print_function

"""
@summary: submit many contract.set(arg) transactions to the example contract

@version: v04
@since:   17/April/2018
@author:  https://github.com/drandreaskrueger
"""

from web3 import Web3, HTTPProvider
import sys, time, threading

RPCaddress='http://localhost:22001' # node 1 of the 7nodes quorum example

# HTTP provider 
# (TODO: try IPC provider, perhaps done within the docker container?)
web3 = Web3(HTTPProvider(RPCaddress, request_kwargs={'timeout': 120}))
print("BlockNumber = ", web3.eth.blockNumber)

def unlockAccount(address=None, password="", duration=3600):
    """
    unlock once, then leave open, to not loose time for unlocking
    """
    if not address:
        address = web3.eth.coinbase
    return web3.personal.unlockAccount(address, password, duration)


def initialize(contractTx_blockNumber=1, contractTx_transactionIndex=0):
    """
    use example contract from 7 nodes example
    if called without arguments, it assumes that the very first transaction was done by
    ./runscript.sh script1.js
    """
    abi = [{"constant":True,"inputs":[],"name":"storedData","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"x","type":"uint256"}],"name":"set","outputs":[],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"get","outputs":[{"name":"retVal","type":"uint256"}],"payable":False,"type":"function"},{"inputs":[{"name":"initVal","type":"uint256"}],"type":"constructor"}];
    
    print ("Getting the address of the example contract that was deployed")
    block = web3.eth.getBlock(contractTx_blockNumber)
    transaction0=block["transactions"][contractTx_transactionIndex]
    print ("transaction hash = ", transaction0)
    address=web3.eth.getTransactionReceipt(transaction0)["contractAddress"]
    print ("contract address = ", address)
    contract = web3.eth.contract(address=address, abi=abi)
    print (contract)
   
    print("unlock account:", unlockAccount())

    return contract


def contract_set(contract, arg, privateFor=None):
    """
    call the .set(arg) method, possibly with 'privateFor' tx-property 
    """
    txParameters = {'from': web3.eth.coinbase}
    if privateFor:
        txParameters['privateFor'] = privateFor
    tx = contract.transact(txParameters).set( arg )
    return tx


def many_transactions(howMany):
    """
    naive approach, blocking --> 15 TPS
    """

    contract = initialize()
    
    for i in range(howMany):
        tx = contract_set(contract, 7)
        print ("set() transaction submitted: ", tx)


def many_transactions_threaded(howMany):
    """
    submit many transactions multi-threaded.
    """

    contract = initialize()
    
    threads = []

    for i in range(howMany):
        t = threading.Thread(target = contract_set,
                             args   = (contract, 7))
        threads.append(t)
        print (".", end="")
    
    print ("%d transaction threads created." % len(threads))

    for t in threads:
        t.start()
    print ("all threads started.")
    
    for t in threads: 
        t.join()
        
    print ("all threads ended.")
    

if __name__ == '__main__':
    
    if len(sys.argv)>1 and sys.argv[1]=="threaded1":
        many_transactions_threaded(1000)
    else:
        many_transactions(100)

    


