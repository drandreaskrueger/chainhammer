import os, timeit, shutil, threading, json, time
from hammer.config import RPCaddress
import hammer.tps as tps
from hammer.deploy import FILE_CONTRACT_ADDRESS

from hammer.clienttools import web3connection
answer = web3connection(RPCaddress=RPCaddress)
global w3, NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID 
w3, chainInfos  = answer
NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID = chainInfos

# current path one up?
# unfortunately path if different depending on how py.test is called
path=os.path.abspath(os.curdir)
if os.path.split(path)[-1]=="tests":
    os.chdir("..") 
    

def test_loopUntil_NewContract():
    """
    sorry for complex test
    
    It cannot be tested easily because it's an infinite loop 
    until a contract is deployed, from the second script deploy.py
    
    BUT
    I found a clever way, using another thread to start the looping.
    """
    # better make backup perhaps 
    try: shutil.move(FILE_CONTRACT_ADDRESS, FILE_CONTRACT_ADDRESS+".backup")
    except: pass

    json.dump({"address": "address-dummy ONE"}, open(FILE_CONTRACT_ADDRESS, 'w'))
    
    print ("start loopUntil_NewContract() in its own thread")
    T = threading.Thread(target=tps.loopUntil_NewContract)
    T.start()
    time.sleep(0.2)
    print ("t.is_alive()", T.is_alive())
    
    assert T.is_alive() # endless loop IS running

    # overwriting the file with new content should trigger the thread T to end    
    json.dump({"address": "address-dummy TWO"}, open(FILE_CONTRACT_ADDRESS, 'w'))
    time.sleep(0.3) # perhaps not long enough, for slow filesystems?
    print ("T.is_alive()", T.is_alive())
    
    assert not T.is_alive() # loop is finished
    
    # remove dummy file, and possibly recover backup
    os.remove (FILE_CONTRACT_ADDRESS)
    try: shutil.move(FILE_CONTRACT_ADDRESS+".backup", FILE_CONTRACT_ADDRESS)
    except: pass
    
    
def test_timestampToSeconds_default():
    assert 1 == tps.timestampToSeconds(1, NODENAME="Geth", CONSENSUS="clique")


def test_timestampToSeconds_raft():
    assert 1 == tps.timestampToSeconds(1000000000, NODENAME="Quorum", CONSENSUS="raft")
    

def test_timestampToSeconds_testrpc():
    assert 1 == tps.timestampToSeconds(205, NODENAME="TestRPC", CONSENSUS="whatever")
    
    
def sendMoney_andWaitForReceipt(how_often=1, 
                                amount=0): # amount zero because in parity-deploy 
                                           # the default account has no money yet, see  
                                           # https://github.com/paritytech/parity-deploy/issues/86
    """
    Send a tiny amount of money. Possibly many times. 
    Used for testing:
    
    Without ANY transaction, (in e.g. testRPC or raft) 
    there would not be a second block.
    So ... make block/s by sending transaction/s. 
    """
    txParameters = {'from': w3.eth.defaultAccount,
                    'to':   w3.eth.defaultAccount,
                    'gas' : 90000,
                    'value': amount}
    for i in range(how_often):
        hash = w3.eth.sendTransaction(txParameters)
    if i>1:
        print ("%d transactions sent, the last one being:" % how_often)
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
    
    
def test_measurement_NotTestableBecauseInfiniteLoop():
    """
    cannot be tested? as it is an infinite loop
    """
    # loop = tps.measurement(blockNumber, pauseBetweenQueries=0.3)
    assert True
    