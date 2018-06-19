#!/usr/bin/env python3
# from __future__ import print_function

"""
@summary: Timing transactions that are getting into the chain

@version: v16 (18/June/2018)
@since:   17/April/2018
@organization: electron.org.uk
@author:  https://github.com/drandreaskrueger
@see: https://gitlab.com/electronDLT/chainhammer for updates
"""


import time, timeit, sys
from pprint import pprint

from web3 import Web3, HTTPProvider
from config import printVersions
from deploy import loadFromDisk

from config import RPCaddress2, RAFT

from deploy import setGlobalVariables_clientType # TODO: refactor into tools library?
    

def loopUntilActionBegins_raft(blockNumber_start, query_intervall = 0.1):
    """
    raft:  polls until chain moves forward
    other: polls until a non-empty block appears (untested)
    """
    while(True):
        blockNumber=w3.eth.blockNumber
        
        # relies on chain moving forward only with new transaction, 
        # doesn't work for PoW, works for raft
        if (blockNumber != blockNumber_start):
            break
        
        time.sleep(query_intervall)
      
    print('')
    return blockNumber_start + 1


def loopUntilActionBegins_withNewContract(blockNumber_start, query_intervall = 0.1):
    """
    (UNTESTED!)
    """
    
    AddressAndABI = loadFromDisk()
    
    while(True):
        time.sleep(query_intervall)
        
        # checks whether a new contract has been deployed
        # because then a new address has been saved:
        if (loadFromDisk() != AddressAndABI):
            break
        
    print('')
    return w3.eth.blockNumber # ignore blockNumber_start



def loopUntilActionBegins(blockNumber_start, query_intervall = 0.1):
    if RAFT:
        return loopUntilActionBegins_raft(blockNumber_start, query_intervall=query_intervall)
    else:
        return loopUntilActionBegins_withNewContract(blockNumber_start, query_intervall=query_intervall)


def analyzeNewBlocks(blockNumber, newBlockNumber, txCount, start_time):
    """
    iterate through all new blocks, add up number of transactions
    print status line
    """
    
    txCount_new = 0
    for bl in range(blockNumber+1, newBlockNumber+1):
        txCount_new += w3.eth.getBlockTransactionCount(bl)

    ts_blockNumber =    w3.eth.getBlock(   blockNumber).timestamp
    ts_newBlockNumber = w3.eth.getBlock(newBlockNumber).timestamp
    
    # quorum raft consensus ... returns not seconds but nanoseconds?  
    timeunits = 1000000000.0 if CONSENSUS=="raft" else 1.0
    
    blocktimeSeconds = (ts_newBlockNumber - ts_blockNumber) / timeunits
    
    tps_current = txCount_new / blocktimeSeconds

    txCount += txCount_new
    elapsed = timeit.default_timer() - start_time
    tps = txCount / elapsed
    line = "block %d | new #TX %3d / %4.0f ms = %5.1f TPS_current | total: #TX %4d / %4.1f s = %5.1f TPS_average" 
    line = line % ( blockNumber, txCount_new, blocktimeSeconds * 1000, tps_current, txCount, elapsed, tps) 
    print (line)
    
    return txCount


def measurement(blockNumber, pauseBetweenQueries=0.3):
    """
    when a (or more) new block appeared, 
    add them to the total, and print a line.
    """

    # the block we had been waiting for already contains the first transaction/s
    # N.B.: slight inaccurracy of time measurement, because not measured how long those needed
    txCount=w3.eth.getBlockTransactionCount(blockNumber)
    
    # perhaps instead of elapsed system time, use blocktime?
    start_time = timeit.default_timer() 
    
    print('starting timer, at block', blockNumber, 'which has ', txCount,' transactions; at timecode', start_time)
    
    while(True):
        # wait for empty blocks (untested)
        # does not work in RAFT because there are no empty blocks
        # if(w3.eth.getBlockTransactionCount('latest')==0):
        #    break
        
        # when a new block appears:
        newBlockNumber=w3.eth.blockNumber
        if(blockNumber!=newBlockNumber):
            txCount = analyzeNewBlocks(blockNumber, newBlockNumber, txCount, start_time)
            blockNumber = newBlockNumber

        time.sleep(pauseBetweenQueries) # do not query too often; as little side effect on node as possible 
    
    # In case of RAFT (no empty blocks), it never gets here !
    print ("end")


if __name__ == '__main__':
    printVersions()
    
    global w3
    w3 = Web3(HTTPProvider(RPCaddress2))
    
    global NODENAME, NODETYPE, CONSENSUS, CHAINNAME
    NODENAME, NODETYPE, CONSENSUS, CHAINNAME = setGlobalVariables_clientType(w3)
    
    blockNumber_start = w3.eth.blockNumber
    print ("\nBlock ",blockNumber_start," - waiting for something to happen") 
    
    blocknumber_start_here = loopUntilActionBegins(blockNumber_start) 
    
    # measurement( blockNumber_start + 1 )
    measurement( blocknumber_start_here )
    
    