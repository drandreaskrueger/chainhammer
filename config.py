#!/usr/bin/env python3
"""
@summary: deploy contract

@version: v09 (2/May/2018)
@since:   8/May/2018
@organization: electron.org.uk
@author:  https://github.com/drandreaskrueger
@see: https://gitlab.com/electronDLT/chainhammer for updates
"""

##########
# Choices:

RPCaddress, RPCaddress2 = None, None # just for testing, with TestRPCProvider 
RPCaddress, RPCaddress2 = 'http://localhost:22000', 'http://localhost:22001' # use two different nodes for writing and reading  
RPCaddress, RPCaddress2 = 'http://localhost:8545', 'http://localhost:8545'  # 8545 = default Ethereum RPC port

# consensus algorithm
RAFT=False
# RAFT=True

## submit transaction via web3 or directly via RPC
ROUTE = "web3"  # "web3" "RPC" 

# set this to a list of public keys for privateFor-transactions, 
# or to None for public transactions 
PRIVATE_FOR = ["ROAZBWtSacxXQrOe3FGAqJDyJjFePR5ce4TSIzmJ0Bc="]
PRIVATE_FOR = None

# contract 7nodes example (probably this is 'SimpleStorage.sol'?)
ABI = [{"constant":True,"inputs":[],"name":"storedData","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"x","type":"uint256"}],"name":"set","outputs":[],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"get","outputs":[{"name":"retVal","type":"uint256"}],"payable":False,"type":"function"},{"inputs":[{"name":"initVal","type":"uint256"}],"type":"constructor"}];
BIN = "0x6060604052341561000f57600080fd5b604051602080610149833981016040528080519060200190919050505b806000819055505b505b610104806100456000396000f30060606040526000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680632a1afcd914605157806360fe47b11460775780636d4ce63c146097575b600080fd5b3415605b57600080fd5b606160bd565b6040518082815260200191505060405180910390f35b3415608157600080fd5b6095600480803590602001909190505060c3565b005b341560a157600080fd5b60a760ce565b6040518082815260200191505060405180910390f35b60005481565b806000819055505b50565b6000805490505b905600a165627a7a72305820d5851baab720bba574474de3d09dbeaabc674a15f4dd93b974908476542c23f00029"

# contract files:
CONTRACT_SOURCE = "contract.sol"
CONTRACT_ABI = "contract-abi.json"
CONTRACT_ADDRESS ="contract-address.json"

# account passphrase
PASSPHRASE_FILE = "account-passphrase.txt"

def printVersions():
    import sys
    from web3 import __version__ as web3version 
    from solc import get_solc_version
    from testrpc import __version__ as ethtestrpcversion
    
    import pkg_resources
    pysolcversion = pkg_resources.get_distribution("py-solc").version
    
    print ("versions: web3 %s, py-solc: %s, solc %s, testrpc %s, python %s" % (web3version, pysolcversion, get_solc_version(), ethtestrpcversion, sys.version.replace("\n", "")))


if __name__ == '__main__':
    printVersions()
    print ("Do not run this. Like you just did. Don't.")
    
    