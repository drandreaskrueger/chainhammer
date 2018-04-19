#!/usr/bin/env python
from __future__ import print_function

"""
@summary: Timing transactions that are getting into the chain

@version: v05 (19/April/2018)
@since:   17/April/2018
@author:  https://github.com/drandreaskrueger
"""

from web3 import Web3, HTTPProvider
import time, timeit
from pprint import pprint

# HTTP provider 
RPCaddress='http://localhost:22002' # node 2 of the 7nodes quorum example

web3 = Web3(HTTPProvider(RPCaddress))
blockNumber_start=web3.eth.blockNumber
RAFT=True

print ("\nBlock ",blockNumber_start," - waiting for something to happen") 
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
    
    time.sleep(0.1)
  
print('')

blockNumber=blockNumber_start+1 # the first new block 
start_time = timeit.default_timer()
txCount=web3.eth.getBlockTransactionCount(blockNumber)
print('starting timer, at block', blockNumber, 'which has ', txCount,' transactions; at timecode', start_time)

while(True):
    # does not work in RAFT:
    if(web3.eth.getBlockTransactionCount('latest')==0):
        break
    
    # if a new block appears:
    newBlockNumber=web3.eth.blockNumber
    
    if(blockNumber!=newBlockNumber):
        
        txCount_new = 0
        for bl in range(blockNumber+1, newBlockNumber+1):
            # add all additional transactions that have entered the blocks
            txCount_new += web3.eth.getBlockTransactionCount(bl)

        ts_blockNumber = web3.eth.getBlock(blockNumber).timestamp
        # pprint (dict(ts_blockNumber)); exit()
        
        ts_newBlockNumber = web3.eth.getBlock(newBlockNumber).timestamp
        duration = (ts_newBlockNumber - ts_blockNumber) 
        tps_current = 1000000000 * txCount_new / duration 

        txCount += txCount_new
        elapsed = timeit.default_timer() - start_time
        tps = txCount / elapsed
        line = "block %d | new #TX %3d / %4.0f ms = %3.0f TPS_current | total: #TX %4d / %4.1f s = %5.1f TPS_average" 
        line = line % ( blockNumber, txCount_new, duration / 1000000, tps_current, txCount, elapsed, tps) 
        print (line)
        blockNumber = newBlockNumber

    time.sleep(0.5) # do not query too often; as little side effect on node as possible 


# In case of RAFT (no empty blocks), it never gets here !
print ("end")
