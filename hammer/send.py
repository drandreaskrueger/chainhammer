#!/usr/bin/env python3
"""
@summary: submit many contract.set(arg) transactions to the example contract

@version: v46 (03/January/2019)
@since:   17/April/2018
@organization: 
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates
"""

# extend sys.path for imports:
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

################
## Dependencies:

# standard library:
import sys, time, random, json
from threading import Thread
from queue import Queue
from pprint import pprint

# pypi:
import requests # pip3 install requests
import web3
from web3 import Web3, HTTPProvider # pip3 install web3
from web3.utils.abi import filter_by_name, abi_to_signature
from web3.utils.encoding import pad_hex

# chainhammer:
from hammer.config import RPCaddress, ROUTE, PRIVATE_FOR, EXAMPLE_ABI
from hammer.config import NUMBER_OF_TRANSACTIONS, PARITY_UNLOCK_EACH_TRANSACTION
from hammer.config import GAS_FOR_SET_CALL
from hammer.config import FILE_LAST_EXPERIMENT, EMPTY_BLOCKS_AT_END
from hammer.deploy import loadFromDisk
from hammer.clienttools import web3connection, unlockAccount


##########################
## smart contract related:


def initialize_fromAddress():
    """
    initialise contract object from address, stored in disk file by deploy.py
    """
    contractAddress, abi = loadFromDisk()
    myContract = w3.eth.contract(address=contractAddress,
                                 abi=abi)
    return myContract
    

def contract_set_via_web3(contract, arg, hashes = None, privateFor=PRIVATE_FOR, gas=GAS_FOR_SET_CALL):
    """
    call the .set(arg) method, possibly with 'privateFor' tx-property
    using the web3 method 
    """
    txParameters = {'from': w3.eth.defaultAccount,
                    'gas' : gas}
    if privateFor:
        txParameters['privateFor'] = privateFor  # untested
        
    # pprint (txParameters)
    
    if PARITY_UNLOCK_EACH_TRANSACTION:
        unlockAccount()
        
    tx = contract.functions.set( x=arg ).transact(txParameters)
    print ("[sent via web3]", end=" ")  # TODO: not print this here but at start
    tx = w3.toHex(tx)
    
    if not hashes==None:
        hashes.append(tx)
    return tx


def try_contract_set_via_web3(contract, arg=42):
    """
    test the above
    """
    tx = contract_set_via_web3(contract, arg=arg)
    print (tx)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx)
    storedData = contract.functions.get().call()
    print (storedData) 
    return storedData


## Manually build & submit transaction, i.e. not going though web3
## (the hope of @jpmsam was that this would speed it up) 
## 
## Note that the data compilation steps are already implemented as
## myContract.functions.myMethod(*args, **kwargs).buildTransaction(transaction)
## but the following bypasses web3.py completely!


def contract_method_ID(methodname, abi):
    """
    build the 4 byte ID, from abi & methodname
    """
    method_abi = filter_by_name(methodname, abi)
    assert(len(method_abi)==1)
    method_abi = method_abi[0]
    method_signature = abi_to_signature(method_abi) 
    method_signature_hash_bytes = w3.sha3(text=method_signature) 
    method_signature_hash_hex = w3.toHex(method_signature_hash_bytes)
    method_signature_hash_4bytes = method_signature_hash_hex[0:10]
    return method_signature_hash_4bytes


def argument_encoding(contract_method_ID, arg):
    """
    concatenate method ID + padded parameter
    """
    arg_hex = w3.toHex(arg)
    arg_hex_padded = pad_hex ( arg_hex, bit_size=256)
    data = contract_method_ID + arg_hex_padded [2:]
    return data
    
    
def timeit_argument_encoding():
    """
    test the above:
    'Doing that 10000 times ... took 0.45 seconds'
    """
    timer = time.clock()
    reps = 10000
    for i in range(reps):
        method_ID = contract_method_ID("set", ABI)
        data = argument_encoding(method_ID, 7)
    timer = time.clock() - timer
    print (data)
    # no need to precalculate, it takes near to no time:
    print ("Doing that %d times ... took %.2f seconds" % (reps, timer) )


def contract_set_via_RPC(contract, arg, hashes = None, privateFor=PRIVATE_FOR, gas=GAS_FOR_SET_CALL):
    """
    call the .set(arg) method numTx=10
    not going through web3
    but directly via RPC
    
    suggestion by @jpmsam 
    https://github.com/jpmorganchase/quorum/issues/346#issuecomment-382216968
    """
    
    method_ID = contract_method_ID("set", contract.abi) # TODO: make this "set" flexible for any method name
    data = argument_encoding(method_ID, arg)
    txParameters = {'from': w3.eth.defaultAccount, 
                    'to' : contract.address,
                    'gas' : w3.toHex(gas),
                    'data' : data} 
    if privateFor:
        txParameters['privateFor'] = privateFor  # untested
    
    method = 'eth_sendTransaction'
    payload= {"jsonrpc" : "2.0",
               "method" : method,
               "params" : [txParameters],
               "id"     : 1}
    headers = {'Content-type' : 'application/json'}
    response = requests.post(RPCaddress, json=payload, headers=headers)
    # print('raw json response: {}'.format(response.json()))
    tx = response.json()['result']
        
    print ("[sent directly via RPC]", end=" ") # TODO: not print this here but at start
    
    if not hashes==None:
        hashes.append(tx)
    return tx


def try_contract_set_via_RPC(contract, steps=3):
    """
    test the above, write 3 transactions, and check the storedData
    """
    rand = random.randint(1, 100)
    for number in range(rand, rand+steps):
        tx = contract_set_via_RPC(contract, number)
        print ("after setat(%d) tx" % number, tx, " the storedData now is", end=" ")
        # TODO: wait for receipt!
        storedData = contract.functions.get().call()
        print (storedData) 
    
    
    
# CHOOSE which route to choose (web3 / RPC) depending on constant ROUTE
contract_set = contract_set_via_web3   if ROUTE=="web3" else contract_set_via_RPC


################################################################
### 
### benchmarking routines 
###
### 0 blocking
### 1 async 
### 2 async, queue, can give number of workers
### 3 async, batched (obsolete)
###
################################################################


def many_transactions_consecutive(contract, numTx):
    """
    naive approach, blocking --> 15 TPS
    """
    print ("send %d transactions, non-async, one after the other:\n" % (numTx))
    txs = []
    for i in range(numTx):
        tx = contract_set(contract, i)
        print ("set() transaction submitted: ", tx) # Web3.toHex(tx)) # new web3
        txs.append(tx)
    return txs
        


def many_transactions_threaded(contract, numTx):
    """
    submit many transactions multi-threaded.
    
    N.B.: 1 thread / transaction 
          --> machine can run out of threads, then crash
    """
    
    print ("send %d transactions, multi-threaded, one thread per tx:\n" % (numTx))

    threads = []
    txs = [] # container to keep all transaction hashes
    for i in range(numTx):
        t = Thread(target = contract_set,
                   args   = (contract, i, txs))
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
    
    return txs

def many_transactions_threaded_Queue(contract, numTx, num_worker_threads=25):
    """
    submit many transactions multi-threaded, 
    with size limited threading Queue
    """

    line = "send %d transactions, via multi-threading queue with %d workers:\n"
    print (line % (numTx, num_worker_threads))

    q = Queue()
    txs = [] # container to keep all transaction hashes
    
    def worker():
        while True:
            item = q.get()
            contract_set(contract, item, txs)
            print ("T", end=""); sys.stdout.flush()
            q.task_done()

    for i in range(num_worker_threads):
         t = Thread(target=worker)
         t.daemon = True
         t.start()
         print ("W", end=""); sys.stdout.flush()
    print ("\n%d worker threads created." % num_worker_threads)

    for i in range(numTx):
        q.put (i)
        print ("I", end=""); sys.stdout.flush()
    print ("\n%d items queued." % numTx)

    q.join()
    print ("\nall items - done.")
    
    return txs


def many_transactions_threaded_in_batches(contract, numTx, batchSize=25):
    """
    submit many transactions multi-threaded;
    but in batches of rather small numbers.
    
    OBSOLETE <-- not faster than threaded2.  
    """

    line = "send %d transactions, multi-threaded, one thread per tx, " \
           "in batches of %d parallel threads:\n"
    print (line % (numTx, batchSize))
    
    txs = [] # container to keep all transaction hashes
    
    howManyLeft=numTx
    while howManyLeft>0:
    
        line = "Next batch of %d transactions ... %d left to do"    
        print (line % (batchSize, howManyLeft))
        
        threads = []
        
        number = batchSize if howManyLeft>batchSize else howManyLeft 
        
        for i in range(number):
            t = Thread(target = contract_set,
                       args   = (contract, i, txs))
            threads.append(t)
            print (".", end="")
        print ("\n%d transaction threads created." % len(threads))
    
        for t in threads:
            t.start()
            print (".", end="")
            sys.stdout.flush()
        print ("\nall threads started.")
        
        for t in threads: 
            t.join()
        print ("\nall threads ended.")

        howManyLeft -= number
        
    return txs


################################################################
### 
### control sample: have the transactions been SUCCESSFUL ?
###
################################################################


def hasTxSucceeded(tx_receipt): #, gasGiven=GAS_FOR_SET_CALL):
    
    # txReceipt.status or None
    status = tx_receipt.get("status", None) 
    if status == 1:  # clear answer = transaction succeeded!
        return True
    if status == 0:  # clear answer = transaction failed!
        return False

    # unfortunately not all clients support status field yet (e.g. testrpc-py, quorum)
     
    # second way is to compare gasGiven with gasUsed:
    tx_hash=tx_receipt.transactionHash
    gasGiven = w3.eth.getTransaction(tx_hash)["gas"]
    gasLeftOver = tx_receipt.gasUsed < gasGiven
    
    if not gasLeftOver:
        # many types of transaction failures result in all given gas being used up
        # e.g. a failed assert() in solidity leads to all gas used up
        # Then it's clear = transaction failed!
        return False 
    
    if gasLeftOver:
        # THIS is the dangerous case, because 
        # e.g. solidity throw / revert() / require() are also returning some unused gas!
        # As well as SUCCESSFUL transactions are returning some gas!
        # But for clients without the status field, this is the only indicator, so:
        return True
    

def receiptGetter(tx_hash, timeout, resultsDict):
    try:
        resultsDict[tx_hash] = w3.eth.waitForTransactionReceipt(tx_hash, timeout)
    except web3.utils.threads.Timeout:
        pass
        
            
def getReceipts_multithreaded(tx_hashes, timeout):
    """
    one thread per tx_hash
    """
    
    tx_receipts = {}
    print("Waiting for %d transaction receipts, can possibly take a while ..." % len(tx_hashes))
    threads = []    
    for tx_hash in tx_hashes:
        t = Thread(target = receiptGetter,
                   args   = (tx_hash, timeout, tx_receipts))
        threads.append(t)
        t.start()
    
    # wait for all of them coming back:
    for t in threads: 
        t.join()
    
    return tx_receipts


def controlSample_transactionsSuccessful(txs, sampleSize=50, timeout=100):
    """
    Makes sure that the transactions were actually successful, 
    and did not fail because e.g. running out of gas, etc.
    
    We want to benchmark the speed of successful state changes!!
    
    Method: Instead of checking EVERY transaction this just takes some sample.
    It can fail in three very different ways:
    
    * timeout when waiting for tx-receipt, then you try raising the timeout seconds
    * tx_receipt.status == 0 for any of the sampled transactions. Real tx failure!
    * all given gas used up. It's only an indirect indicator for a failed transaction.
    """
    
    print ("Check control sample.")
    N = sampleSize if len(txs)>sampleSize else len(txs) 
    txs_sample = random.sample(txs, N)
    
    tx_receipts = getReceipts_multithreaded(tx_hashes=txs_sample, timeout=timeout) 
    
    # Test 1: Are all receipts here?    
    M = len(tx_receipts)
    if M != N:
        print ("Bad: Timeout, received receipts only for %d out of %d sampled transactions." % (M, N))
        success = False 
    else:
        print ("Good: No timeout, received the receipts for all %d sampled transactions." % N)
        success = True
            
    # Test 2: Was each an every transaction successful?
    badCounter=0
    for tx_hash, tx_receipt in tx_receipts.items():
        # status = tx_receipt.get("status", None) # unfortunately not all clients support this yet
        # print ((tx_hash, status, tx_receipt.gasUsed ))
        if not hasTxSucceeded(tx_receipt):
            success = False
            print ("Transaction NOT successful:", tx_hash, tx_receipt)
            badCounter = badCounter+1 
    # pprint (dict(tx_receipt))

    if badCounter:
        print ("Bad: %d out of %d not successful!" % (badCounter, M))
        
    print ("Sample of %d transactions checked ... hints at:" % M, end=" ")
    print( "TOTAL SUCCESS :-)" if success else "-AT LEAST PARTIAL- FAILURE :-(" )
    
    return success


# Try out the above with
# pytest tests/test_send.py::test_controlSample_transactionsSuccessful


################################################################################
### 
### estimate range of blocks, first and last 100 transaction hashes
###
################################################################################


def getReceipts_multithreaded_Queue(tx_hashes, timeout, num_worker_threads=8, ifPrint=False):
    """
    Query the RPC via a multithreading Queue, with 8 worker threads.
    Advantage over 'getReceipts_multithreaded': 
                       Will also work for len(tx_hashes) > 1000 
    """
    
    start=time.monotonic()
    q = Queue()
    tx_receipts = {}
    
    def worker():
        while True:
            tx_hash = q.get()
            receiptGetter(tx_hash, timeout, tx_receipts)
            q.task_done()

    for i in range(num_worker_threads):
         t = Thread(target=worker)
         t.daemon = True
         t.start()

    for tx in tx_hashes:
        q.put (tx)

    q.join()
    
    if ifPrint:
        duration = time.monotonic() - start
        print ("%d lookups took %.1f seconds" % (len(tx_receipts), duration))
    
    return tx_receipts


def when_last_ones_mined__give_range_of_block_numbers(txs, txRangesSize=100, timeout=60):
    """
    Also only a heuristics:
    Assuming that the first 100 and the last 100 transaction hashes 
    that had been added to the list 'txs'
    can reveal the min and max blocknumbers of this whole experiment
    """

    txs_begin_and_end = txs[:txRangesSize] + txs[-txRangesSize:]
    tx_receipts = getReceipts_multithreaded_Queue(tx_hashes=txs_begin_and_end, 
                                                  timeout=timeout) #, ifPrint=True)
    
    # or actually, all of them? Naaa, too slow:
    #   TestRPC: 2000 lookups took 122.1 seconds
    #    Parity: 2000 lookups took 7.2 seconds
    #      Geth: 2000 lookups took 8.6 seconds
    # tx_receipts = getReceipts_multithreaded_Queue(tx_hashes=txs, 
    #                                              timeout=timeout, ifPrint=True)
    
    blockNumbers = [receipt.blockNumber for receipt in tx_receipts.values()]
    blockNumbers = sorted(list(set(blockNumbers))) # make unique
    # print (blockNumbers) 
    return min(blockNumbers), max(blockNumbers)

    
def store_experiment_data(success, num_txs, 
                          block_from, block_to, 
                          empty_blocks,
                          filename=FILE_LAST_EXPERIMENT):
    """
    most basic data about this last experiment, 
    stored in same (overwritten) file.
    Purpose: diagramming should be able to calc proper averages & select ranges
    """
    data = {"send" : {
                "block_first" : block_from,
                "block_last": block_to,
                "empty_blocks": empty_blocks, 
                "num_txs" : num_txs,
                "sample_txs_successful": success
                },
            "node" : {
                "rpc_address": RPCaddress,
                "web3.version.node": w3.version.node,
                "name" : NODENAME,
                "type" : NODETYPE,
                "version" : NODEVERSION, 
                "consensus" : CONSENSUS, 
                "network_id" : NETWORKID, 
                "chain_name" : CHAINNAME, 
                "chain_id" : CHAINID
                }
            }
            
    with open(filename, "w") as f:
        json.dump(data, f)
    

def wait_some_blocks(waitBlocks=EMPTY_BLOCKS_AT_END, pauseBetweenQueries=0.3):
    """
    Actually, the waiting has to be done here, 
    because ./send.py is started later than ./tps.py
    So when ./send.py ends, the analysis can happen.
    """
    blockNumber_start = w3.eth.blockNumber
    print ("blocknumber now:", blockNumber_start, end=" ")
    print ("waiting for %d empty blocks:" % waitBlocks)
    bn_previous=bn_now=blockNumber_start
    
    while bn_now < waitBlocks + blockNumber_start:
        time.sleep(pauseBetweenQueries)
        bn_now=w3.eth.blockNumber
        # print (bn_now, waitBlocks + blockNumber_start)
        if bn_now!=bn_previous:
            bn_previous=bn_now
            print (bn_now, end=" "); sys.stdout.flush()
         
    print ("Done.")

        
def finish(txs, success):
    block_from, block_to = when_last_ones_mined__give_range_of_block_numbers(txs)
    txt = "Transaction receipts from beginning and end all arrived. Blockrange %d to %d."
    txt = txt % (block_from, block_to)
    print (txt)
    
    if NODETYPE=="TestRPC":
        print ("Do not wait for empty blocks, as this is TestRPC.")
        waitBlocks=0
    else:
        waitBlocks=EMPTY_BLOCKS_AT_END
        wait_some_blocks(waitBlocks)
    
    store_experiment_data (success, len(txs), block_from, block_to, empty_blocks=waitBlocks)
    # print ("Data stored. This will trigger tps.py to end in ~ %d blocks." % EMPTY_BLOCKS_AT_END)
    
    print ("Data stored. This will trigger tps.py to end.\n"
           "(Beware: Wait ~0.5s until tps.py stops and writes to same file.)")
    #          see tps.py --> pauseBetweenQueries=0.3


################################################################################
###
### choose, depending on CLI parameter
###
################################################################################

def sendmany(numTransactions = NUMBER_OF_TRANSACTIONS):

    print("\nBlockNumber = ", w3.eth.blockNumber)
    
    if len(sys.argv)==1 or sys.argv[1]=="sequential":
        
        # blocking, non-async
        txs=many_transactions_consecutive(contract, numTransactions)  
        
    elif sys.argv[1]=="threaded1":
        txs=many_transactions_threaded(contract, numTransactions)
            
            
    elif sys.argv[1]=="threaded2":
        num_workers = 100
        if len(sys.argv)>2:
            try:
                num_workers = int(sys.argv[2])
            except:
                pass
            
        txs=many_transactions_threaded_Queue(contract, 
                                         numTx=numTransactions, 
                                         num_worker_threads=num_workers)
        
    elif sys.argv[1]=="threaded3":
        batchSize=25
        txs=many_transactions_threaded_in_batches(contract, 
                                              numTx=numTransactions, 
                                              batchSize=batchSize)
          
    else:
        print ("Nope. Choice '%s'" % sys.argv[1], "not recognized.")

        
    print ("%d transaction hashes recorded, examples: %s" % (len(txs), txs[:2]))
    
    return txs


if __name__ == '__main__':

    global w3, NODENAME, NODETYPE, NODEVERSION, CONSENSUS, NETWORKID, CHAINNAME, CHAINID
    w3, chainInfos = web3connection(RPCaddress=RPCaddress, account=None)
    NODENAME, NODETYPE, NODEVERSION, CONSENSUS, NETWORKID, CHAINNAME, CHAINID = chainInfos

    # wait_some_blocks(0); exit()


    w3.eth.defaultAccount = w3.eth.accounts[0] # set first account as sender
    # timeit_argument_encoding(); exit()
    
   
    contract = initialize_fromAddress()
        
    # try_contract_set_via_web3(contract); exit()
    # try_contract_set_via_RPC(contract);  exit()

    txs = sendmany()

    success = controlSample_transactionsSuccessful(txs)

    finish(txs, success)
    
    