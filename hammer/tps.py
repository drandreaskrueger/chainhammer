#!/usr/bin/env python3
# from __future__ import print_function

"""
@summary: Timing transactions that are getting into the chain

@version: v43 (16/December/2018)
@since:   17/April/2018
@organization: 
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates
"""


import time, timeit, sys, os

from web3 import Web3, HTTPProvider

# extend path for imports:
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    
from hammer.config import RPCaddress2 
from hammer.deploy import loadFromDisk, FILE_CONTRACT_ADDRESS
from hammer.clienttools import web3connection, getBlockTransactionCount
    

def loopUntil_NewContract(query_intervall = 0.1):
    """
    Wait for new smart contract to be deployed.
    
    Continuously polls file "FILE_CONTRACT_ADDRESS".
    Returns when overwritten file has different address or new filedate.
    
    N.B.: It actually happens that same Ethereum contract address is created again, 
          if blockchain is deleted, and everything restarted. So: Check filedate too.
    """
    
    address, _ = loadFromDisk()
    when = os.path.getmtime(FILE_CONTRACT_ADDRESS) 
    print ("(filedate %d) last contract address: %s" %(when, address)) 
    
    while(True):
        time.sleep(query_intervall)
        
        # checks whether a new contract has been deployed
        # because then a new address has been saved to file:
        newAddress, _ = loadFromDisk()
        newWhen = os.path.getmtime(FILE_CONTRACT_ADDRESS)
        if (newAddress != address or newWhen != when):
            print ("(filedate %d) new contract address: %s" %(newWhen, newAddress))  
            break
    return



def timestampToSeconds(timestamp, NODENAME, CONSENSUS):
    """
    turn timestamp into (float of) seconds
    as a separate function so that it can be recycled in blocksDB_create.py
    """
        
    # most ethereum clients return block timestamps as whole seconds:
    timeunits = 1.0
    
    # quorum raft consensus ... returns not seconds but nanoseconds?
    if CONSENSUS=="raft": timeunits = 1000000000.0
    
    # testrpc-py has odd timestamp units ;-)
    # do check for updates: https://github.com/pipermerriam/eth-testrpc/issues/117
    if NODENAME=="TestRPC": timeunits = 205.0
    
    return timestamp / timeunits
 

def analyzeNewBlocks(blockNumber, newBlockNumber, txCount, start_time):
    """
    iterate through all new blocks, add up number of transactions
    print status line
    """
    
    txCount_new = 0
    for bl in range(blockNumber+1, newBlockNumber+1): # TODO check range again - shift by one? 
        # txCount_new += w3.eth.getBlockTransactionCount(bl)
        blktx = getBlockTransactionCount(w3, bl)
        txCount_new += blktx 

    ts_blockNumber =    w3.eth.getBlock(   blockNumber).timestamp
    ts_newBlockNumber = w3.eth.getBlock(newBlockNumber).timestamp
    ts_diff = ts_newBlockNumber - ts_blockNumber
    
    blocktimeSeconds = timestampToSeconds(ts_diff, NODENAME, CONSENSUS) 

    try:
        tps_current = txCount_new / blocktimeSeconds
    except ZeroDivisionError:
        # Odd: Parity seems to have a blocktime resolution of whole seconds??
        # So if blocks come much faster (e.g. with instantseal), 
        # then they end up having a blocktime of zero lol.
        # Then, set TPS_CURRENT to something wrong but syntactically correct.  
        tps_current = 0

    txCount += txCount_new
    elapsed = timeit.default_timer() - start_time
    tps = txCount / elapsed
    line = "block %d | new #TX %3d / %4.0f ms = " \
           "%5.1f TPS_current | total: #TX %4d / %4.1f s = %5.1f TPS_average" 
    line = line % ( blockNumber, txCount_new, blocktimeSeconds * 1000, 
                    tps_current, txCount, elapsed, tps) 
    print (line)
    
    return txCount


def measurement(blockNumber, pauseBetweenQueries=0.3):
    """
    when a (or more) new block appeared, 
    add them to the total, and print a line.
    """

    # the block we had been waiting for already contains the first transaction/s
    # N.B.: slight inaccurracy of time measurement, because not measured how long those needed
    
    # txCount=w3.eth.getBlockTransactionCount(blockNumber)
    txCount=getBlockTransactionCount(w3, blockNumber)
    
    start_time = timeit.default_timer()
    # TODO: perhaps additional to elapsed system time, show blocktime? 
    
    print('starting timer, at block', blockNumber, 'which has ', 
          txCount,' transactions; at timecode', start_time)
    
    while(True):
        newBlockNumber=w3.eth.blockNumber
        
        if(blockNumber!=newBlockNumber): # when a new block appears:
            txCount = analyzeNewBlocks(blockNumber, newBlockNumber, txCount, start_time)
            blockNumber = newBlockNumber

        time.sleep(pauseBetweenQueries) # do not query too often; as little side effect on node as possible 

        # TODO: allow for an exit condition? 7 consecutive empty blocks?
        
    print ("end")   # N.B.: it never gets here !


if __name__ == '__main__':
    
    global w3, NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID
    w3, chainInfos = web3connection(RPCaddress=RPCaddress2, account=None)
    NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID = chainInfos
    
    blockNumber_before = w3.eth.blockNumber
    print ("\nBlock ",blockNumber_before," - waiting for something to happen") 
    
    loopUntil_NewContract()
    blocknumber_start_here = w3.eth.blockNumber 
    print ("\nblocknumber_start_here =", blocknumber_start_here)
    
    measurement( blocknumber_start_here )
    
    