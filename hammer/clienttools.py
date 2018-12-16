#!/usr/bin/env python3
"""
@summary: tools to talk to an Ethereum client node 

@version: v43 (16/December/2018)
@since:   19/June/2018
@organization: 
@author:  https://github.com/drandreaskrueger
@see: https://github.com/drandreaskrueger/chainhammer for updates
"""


################
## Dependencies:

from pprint import pprint

try:
    from web3 import Web3, HTTPProvider # pip3 install web3
except:
    print ("Dependencies unavailable. Start virtualenv first!")
    exit()

# extend sys.path for imports:
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from hammer.config import RPCaddress, PASSPHRASE_FILE, PARITY_UNLOCK_EACH_TRANSACTION
from hammer.clienttype import clientType

################
## Tools:


def printVersions():
    import sys
    from web3 import __version__ as web3version 
    from solc import get_solc_version
    from testrpc import __version__ as ethtestrpcversion
    
    import pkg_resources
    pysolcversion = pkg_resources.get_distribution("py-solc").version
    
    print ("versions: web3 %s, py-solc: %s, solc %s, testrpc %s, python %s" % (web3version, pysolcversion, get_solc_version(), ethtestrpcversion, sys.version.replace("\n", "")))


################################################################################
# get a connection, and find out as much as possible


def start_web3connection(RPCaddress=None, account=None):
    """
    get a web3 object, and make it global 
    """
    global w3
    if RPCaddress:
        # HTTP provider 
        # (TODO: also try whether IPC provider is faster, when quorum-outside-vagrant starts working)
        w3 = Web3(HTTPProvider(RPCaddress, request_kwargs={'timeout': 120}))
    else:
        # w3 = Web3(Web3.EthereumTesterProvider()) # does NOT work!
        w3 = Web3(Web3.TestRPCProvider()) 
    
    print ("web3 connection established, blockNumber =", w3.eth.blockNumber, end=", ")
    print ("node version string = ", w3.version.node)
    accountname="chosen"
    if not account:
        w3.eth.defaultAccount = w3.eth.accounts[0] # set first account as sender
        accountname="first"
    print (accountname + " account of node is", w3.eth.defaultAccount, end=", ")
    print ("balance is %s Ether" % w3.fromWei(w3.eth.getBalance(w3.eth.defaultAccount), "ether"))
    
    return w3


def setGlobalVariables_clientType(w3):
    """
    Set global variables.
    """
    global NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID
    
    NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID = clientType(w3)
    
    formatter="nodeName: %s, nodeType: %s, consensus: %s, network: %s, chainName: %s, chainId: %s" 
    print (formatter % (NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID))
    
    return NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID # for when imported into other modules


def if_poa_then_bugfix(w3, NODENAME, CHAINNAME, CONSENSUS):
    """
    bugfix for quorum web3.py problem, see
    https://github.com/ethereum/web3.py/issues/898#issuecomment-396701172
    and
    https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority
    
    actually also appeared when using dockerized standard geth nodes with PoA   
    https://github.com/javahippie/geth-dev (net_version='500')
    """
    if NODENAME == "Quorum" or CHAINNAME=='500' or CONSENSUS=='clique':
        from web3.middleware import geth_poa_middleware
        # inject the poa compatibility middleware to the innermost layer
        w3.middleware_stack.inject(geth_poa_middleware, layer=0)


# def web3connection(RPCaddress=RPCaddress, account=None):
def web3connection(RPCaddress=None, account=None):    
    """
    prints dependency versions, starts web3 connection, identifies client node type, if quorum then bugfix
    """
    
    printVersions()
    
    w3 = start_web3connection(RPCaddress=RPCaddress, account=account) 

    NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID = setGlobalVariables_clientType(w3)

    if_poa_then_bugfix(w3, NODENAME, CHAINNAME, CONSENSUS)
    
    chainInfos = NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID
    
    return w3, chainInfos 


################################################################################
# generally useful tools


def getBlockTransactionCount(w3, blockNumber):
    """
    testRPC does not provide this endpoint yet, so replicate its functionality:
    """
    block=w3.eth.getBlock(blockNumber)
    # pprint (block)
    return len(block["transactions"])
    

def unlockAccount(duration=3600, account=None):
    """
    unlock once, then leave open, to later not loose time for unlocking
    """
    
    if "TestRPC" in w3.version.node:
        return True # TestRPC does not need unlocking
    
    if not account:
        account = w3.eth.defaultAccount
        # print (account)

    if NODENAME=="Quorum":
        passphrase=""
    else:
        with open(PASSPHRASE_FILE, "r") as f:
            passphrase=f.read().strip()

    if NODENAME=="Geth" and CONSENSUS=="clique" and NETWORKID==500:
        passphrase="pass" # hardcoded in geth-dev/docker-compose.yml

    # print ("passphrase:", passphrase)

    if PARITY_UNLOCK_EACH_TRANSACTION:
        answer = w3.personal.unlockAccount(account=account, 
                                           passphrase=passphrase)
    else:
        if NODETYPE=="Parity": 
            duration = w3.toHex(duration)
        answer = w3.personal.unlockAccount(account=account, 
                                           passphrase=passphrase,
                                           duration=duration)
    print ("unlocked:", answer)
    return answer
     


if __name__ == '__main__':

    # example how to call this:
    # answer = web3connection()
    answer = web3connection(RPCaddress=RPCaddress, account=None)
    
    w3, chainInfos  = answer
    
    global NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID
    NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID = chainInfos


