#!/usr/bin/env python3
# from __future__ import print_function

"""
@summary: submit many contract.set(arg) transactions to the example contract

@version: v05 (19/April/2018)
@since:   17/April/2018
@author:  https://github.com/drandreaskrueger
"""

RPCaddress='http://localhost:22001' # 22001 = node 1 of the 7nodes quorum example

from web3 import Web3, HTTPProvider # pip3 install web3
import sys, time
from threading import Thread
from queue import Queue
from pprint import pprint


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
    print ("transaction hash = ", Web3.toHex(transaction0))
    address=web3.eth.getTransactionReceipt(transaction0)["contractAddress"]
    print ("contract address = ", address)
    contract = web3.eth.contract(address=address, abi=abi)
    print (contract)
   
    print("unlock account:", unlockAccount())

    # pprint (dir(contract))
    return contract


def contract_set(contract, arg, privateFor=None):
    """
    call the .set(arg) method, possibly with 'privateFor' tx-property 
    """
    txParameters = {'from': web3.eth.coinbase}
    if privateFor:
        txParameters['privateFor'] = privateFor
        
    # old web3 syntax:
    # tx = contract.transact(txParameters).set( arg )
    # new web3 syntax
    tx = contract.functions.set( arg ).transact(txParameters)
    return tx


def many_transactions(contract, howMany):
    """
    naive approach, blocking --> 15 TPS
    """
    
    print ("send %d transactions, non-async, one after the other:\n" % (howMany))

    for i in range(howMany):
        tx = contract_set(contract, 7)
        
        # print ("set() transaction submitted: ", tx) # old web3 
        print ("set() transaction submitted: ", Web3.toHex(tx)) # new web3


def many_transactions_threaded(contract, howMany):
    """
    submit many transactions multi-threaded.
    """

    print ("send %d transactions, multi-threaded, one thread per tx:\n" % (howMany))

    threads = []
    for i in range(howMany):
        t = Thread(target = contract_set,
                   args   = (contract, 7))
        threads.append(t)
        print (".", end="")
    print ("%d transaction threads created." % len(threads))

    for t in threads:
        t.start()
        print (".", end="")
        sys.stdout.flush()
    print ("all threads started.")
    
    for t in threads: 
        t.join()
    print ("all threads ended.")
    

def many_transactions_threaded_Queue(contract, howMany, num_worker_threads=100):
    """
    submit many transactions multi-threaded, 
    with size limited threading Queue
    """

    print ("send %d transactions, via multi-threading queue with %d workers:\n" % (howMany, num_workers))

    q = Queue()
    
    def worker():
        while True:
            item = q.get()
            contract_set(contract, item)
            print (".", end=""); sys.stdout.flush()
            q.task_done()

    for i in range(num_worker_threads):
         t = Thread(target=worker)
         t.daemon = True
         t.start()
         print (".", end=""); sys.stdout.flush()
    print ("%d worker threads created." % num_worker_threads)

    for i in range(howMany):
        q.put (7)
        print (".", end=""); sys.stdout.flush()
    print ("%d items queued." % howMany)

    q.join()
    print ("all items - done.")
    


if __name__ == '__main__':

    # HTTP provider 
    # (TODO: try IPC provider, perhaps done within the docker container?)
    web3 = Web3(HTTPProvider(RPCaddress, request_kwargs={'timeout': 120}))
    print("\nBlockNumber = ", web3.eth.blockNumber)
    
    contract = initialize()

    if len(sys.argv)>1:
        if sys.argv[1]=="threaded1":
            many_transactions_threaded(contract, 1000)
            
            
        elif sys.argv[1]=="threaded2":
            num_workers = 100
            if len(sys.argv)>2:
                try:
                    num_workers = int(sys.argv[2])
                except:
                    pass
            many_transactions_threaded_Queue(contract, 1000, num_worker_threads=num_workers)
            
        else:
            print ("Nope. Choice '%s'" % sys.argv[1], "not recognized.")
    else:
        
        many_transactions(contract, 100)  # blocking, non-async

    


