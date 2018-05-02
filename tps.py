#!/usr/bin/env python3
# from __future__ import print_function

"""
@summary: Timing transactions that are getting into the chain

@version: v05 (19/April/2018)
@since:   17/April/2018
@author:  https://github.com/drandreaskrueger
"""

RPCaddress='http://localhost:22002' # node 2 of the 7nodes quorum example
RAFT=True # # consensus algo - TODO: ask node

import time, timeit, sys
from pprint import pprint

from web3 import Web3, HTTPProvider
from config import printVersions


printVersions()

def loopUntilActionBegins(query_intervall = 0.1):
    """
    raft:  polls until chain moves forward
    other: polls until a non-empty block appears (untested)
    """
    while(True):
        blockNumber=web3.eth.blockNumber
        
        if RAFT:
            # relies on chain moving forward, doesn't work for PoW, works for raft
            if (blockNumber != blockNumber_start):
                break
        else:
            # relies on empty blocks, doesn't work for raft:
            if(web3.eth.getBlockTransactionCount('latest')!=0):
                break
        
        time.sleep(query_intervall)
      
    print('')
    return blockNumber_start + 1


def analyzeNewBlocks(blockNumber, newBlockNumber, txCount, start_time):
    """
    iterate through all new blocks, add up number of transactions
    print status line
    """
    
    txCount_new = 0
    for bl in range(blockNumber+1, newBlockNumber+1):
        txCount_new += web3.eth.getBlockTransactionCount(bl)

    ts_blockNumber =    web3.eth.getBlock(   blockNumber).timestamp
    ts_newBlockNumber = web3.eth.getBlock(newBlockNumber).timestamp
    duration = (ts_newBlockNumber - ts_blockNumber) 
    tps_current = 1000000000.0 * txCount_new / duration 

    txCount += txCount_new
    elapsed = timeit.default_timer() - start_time
    tps = txCount / elapsed
    line = "block %d | new #TX %3d / %4.0f ms = %5.1f TPS_current | total: #TX %4d / %4.1f s = %5.1f TPS_average" 
    line = line % ( blockNumber, txCount_new, duration / 1000000, tps_current, txCount, elapsed, tps) 
    print (line)
    
    return txCount


def measurement(blockNumber, pauseBetweenQueries=0.3):
    """
    when a (or more) new block appeared, 
    add them to the total, and print a line.
    """

    # the block we had been waiting for already contains the first transaction/s
    # N.B.: slight inaccurracy of time measurement, because not measured how long those needed
    txCount=web3.eth.getBlockTransactionCount(blockNumber)
    
    # perhaps instead of elapsed system time, use blocktime?
    start_time = timeit.default_timer() 
    
    print('starting timer, at block', blockNumber, 'which has ', txCount,' transactions; at timecode', start_time)
    
    while(True):
        # wait for empty blocks (untested)
        # does not work in RAFT because there are no empty blocks
        if(web3.eth.getBlockTransactionCount('latest')==0):
            break
        
        # when a new block appears:
        newBlockNumber=web3.eth.blockNumber
        if(blockNumber!=newBlockNumber):
            txCount = analyzeNewBlocks(blockNumber, newBlockNumber, txCount, start_time)
            blockNumber = newBlockNumber

        time.sleep(pauseBetweenQueries) # do not query too often; as little side effect on node as possible 
    
    # In case of RAFT (no empty blocks), it never gets here !
    print ("end")


if __name__ == '__main__':
    
    web3 = Web3(HTTPProvider(RPCaddress))
    
    blockNumber_start = web3.eth.blockNumber
    print ("\nBlock ",blockNumber_start," - waiting for something to happen") 
    
    loopUntilActionBegins() 
    
    measurement( blockNumber_start + 1 )
    
    