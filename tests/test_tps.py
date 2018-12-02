import os, timeit
from config import RPCaddress

from clienttools import web3connection
answer = web3connection(RPCaddress=RPCaddress)
global w3, NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID 
w3, chainInfos  = answer
NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID = chainInfos

import tps

def test_loopUntil_NewContract_HowtoTestThisNoIdea():
    """
    cannot be tested easily because infinite loop 
    until a contract is deployed, from the second script?
    """
    # loopUntil_NewContract(query_intervall = 0.1) 
    assert True
    
    
def test_timestampToSeconds_default():
    assert 1 == tps.timestampToSeconds(1, NODENAME="Geth", CONSENSUS="clique")


def test_timestampToSeconds_raft():
    assert 1 == tps.timestampToSeconds(1000000000, NODENAME="Quorum", CONSENSUS="raft")
    

def test_timestampToSeconds_testrpc():
    assert 1 == tps.timestampToSeconds(205, NODENAME="TestRPC", CONSENSUS="whatever")
    
    
def sendMoney_andWaitForReceipt():
    """
    without ANY transaction, (in e.g. testRPC or raft) there would not be a second block
    so ... make a block 
    """
    txParameters = {'from': w3.eth.defaultAccount,
                    'to':   w3.eth.defaultAccount,
                    'gas' : 90000,
                    'value': 1}
    hash = w3.eth.sendTransaction(txParameters)
    print ("tx sent, hash:", w3.toHex(hash))
    print ("waiting for receipt ...")
    tx_receipt = w3.eth.waitForTransactionReceipt(hash)
    print ("tx_receipt.blockNumber", tx_receipt.blockNumber)
    return hash

    
def test_analyzeNewBlocks():

    sendMoney_andWaitForReceipt() # to generate at least one more block
    
    txCount=0
    start_time = timeit.default_timer()
    tps.w3, tps.NODENAME, tps.CONSENSUS = w3, NODENAME, CONSENSUS 
    answer = tps.analyzeNewBlocks(0, 1, txCount, start_time)
    print (answer)
    assert answer >= 0
    
    
def test_measurement_HowtoTestThisNoIdea():
    """
    cannot be tested? as it is an infinite loop
    """
    assert True
    
    