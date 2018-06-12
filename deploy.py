#!/usr/bin/env python3
"""
@summary: deploy contract

@version: v15 (12/June/2018)
@since:   2/May/2018
@organization: electron.org.uk
@author:  https://github.com/drandreaskrueger
@see: https://gitlab.com/electronDLT/chainhammer for updates
"""


################
## Dependencies:

import sys, time, json
from pprint import pprint

import requests # pip3 install requests

try:
    from web3 import Web3, HTTPProvider # pip3 install web3
    from solc import compile_source # pip install py-solc
except:
    print ("Dependencies unavailable. Start virtualenv first!")
    exit()

from config import RPCaddress, CONTRACT_SOURCE, CONTRACT_ABI, CONTRACT_ADDRESS
from config import PRIVATE_FOR, printVersions, PASSPHRASE_FILE

from clienttype import clientType


###############################################################################
## deploy example from
## http://web3py.readthedocs.io/en/latest/examples.html#working-with-contracts
## when 'latest' was 4.2.0
###############################################################################


def compileContract(contract_source_file):
    """
    Reads file, compiles, returns contract name and interface
    """
    with open(contract_source_file, "r") as f:
        contract_source_code = f.read()
    compiled_sol = compile_source(contract_source_code) # Compiled source code
    assert(len(compiled_sol)==1) # assert source file has only one contract object
    contractName = list(compiled_sol.keys())[0] 
    contract_interface = compiled_sol[contractName]
    return contractName.replace("<stdin>:", ""), contract_interface 


def deployContract(contract_interface, ifPrint=True):
    """
    deploys contract, waits for receipt, returns address
    """
    myContract = w3.eth.contract(abi=contract_interface['abi'], 
                                 bytecode=contract_interface['bin'])
    tx_hash = w3.toHex( myContract.constructor().transact() )
    print ("tx_hash = ", tx_hash, "--> waiting for receipt ...")
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    contractAddress = tx_receipt["contractAddress"]
    if ifPrint:
        print ( "Deployed. gasUsed={gasUsed} contractAddress={contractAddress}".format(**tx_receipt) )
    return contractAddress 

    
def contractObject(contractAddress, abi):
    """
    recreates myContract object when given address on chain, and ABI
    """
    # Create the contract instance with the newly-deployed address
    myContract = w3.eth.contract(address=contractAddress,
                                 abi=abi)
    return myContract
    

##########################
## additional basic tasks:
##########################

def start_web3connection(RPCaddress=None, account=None):
    """
    get a global web3 object
    """
    global w3
    if RPCaddress:
        # HTTP provider 
        # (TODO: also try whether IPC provider is faster, when quorum-outside-vagrant starts working)
        w3 = Web3(HTTPProvider(RPCaddress, request_kwargs={'timeout': 120}))
    else:
        w3 = Web3(Web3.TestRPCProvider()) 
    
    print ("web3 connection established, blockNumber =", w3.eth.blockNumber, end=", ")
    print ("node version string = ", w3.version.node)
    if not account:
        w3.eth.defaultAccount = w3.eth.accounts[0] # set first account as sender
    print ("first account of node is", w3.eth.defaultAccount, end=", ")
    print ("balance is %s Ether" % w3.fromWei(w3.eth.getBalance(w3.eth.defaultAccount), "ether"))
    
    return w3


def saveToDisk(contractAddress, abi):
    """
    save address & abi, for usage in the other script
    """
    json.dump({"address": contractAddress}, open(CONTRACT_ADDRESS, 'w'))
    json.dump(abi, open(CONTRACT_ABI, 'w'))


def loadFromDisk():
    """
    load address & abi from previous run of 'deployTheContract'
    """
    contractAddress = json.load(open(CONTRACT_ADDRESS, 'r'))
    abi = json.load(open(CONTRACT_ABI, 'r'))
    return contractAddress["address"], abi


def unlockAccount(duration=3600):
    """
    unlock once, then leave open, to later not loose time for unlocking
    """
    
    if "TestRPC" in w3.version.node:
        return True # TestRPC does not need unlocking 
    
    account = w3.eth.defaultAccount
        

    if NODENAME=="Quorum":
        passphrase=""
    else:
        with open(PASSPHRASE_FILE, "r") as f:
            passphrase=f.read().strip()

    if NODETYPE=="Parity":
        duration = w3.toHex(duration)

    return w3.personal.unlockAccount(account=account, 
                                     passphrase=passphrase,  
                                     duration=duration)


def deployTheContract(contract_source_file):
    """
    compile, deploy, save
    """
    contractName, contract_interface = compileContract(contract_source_file)
    print ("unlock: ", unlockAccount())
    contractAddress = deployContract(contract_interface)
    saveToDisk(contractAddress, abi=contract_interface["abi"])
    return contractName, contract_interface, contractAddress


def testMethods(myContract):
    """
    just a test if the contract's methods are working
    --> call getter then setter then getter  
    """
    answer = myContract.functions.get().call()
    print('.get(): {}'.format(answer))
    
    print('.set()')
    tx_hash = w3.toHex( myContract.functions.set(answer + 1).transact() )
    print ("transaction", tx_hash, "... "); sys.stdout.flush()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print ("... mined. Receipt --> gasUsed={gasUsed}". format(**tx_receipt) )
    
    answer = myContract.functions.get().call()
    print('.get(): {}'.format(answer))


def setGlobalVariables_clientType():
    """
    set global variables
    """
    global NODENAME, NODETYPE, CONSENSUS
    NODENAME, NODETYPE, CONSENSUS = clientType(w3)
    print ("nodeName: %s, nodeType: %s, consensus: %s" % (NODENAME, NODETYPE, CONSENSUS))
    

if __name__ == '__main__':
    printVersions()
    
    # account=None --> default account [0]
    start_web3connection(RPCaddress=RPCaddress, account=None) 

    setGlobalVariables_clientType()

    deployTheContract(contract_source_file=CONTRACT_SOURCE)
    
    if len(sys.argv)>1 and sys.argv[1]=="notest":
        exit() # argument "notest" allows to skip the .set() test transaction 
        
    contractAddress, abi = loadFromDisk()
    myContract = contractObject(contractAddress, abi)
    testMethods(myContract)
    
    
    