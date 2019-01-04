#!/usr/bin/env python3
"""
@summary: settings

@version: v46 (03/January/2019)
@since:   8/May/2018
@organization: 
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates
"""

##########
# Choices:

# use this for unittesting with TestRPCProvider
RPCaddress, RPCaddress2 = None, None  

# or this for experiment runs OR for unittesting with real Ethereum nodes:
# RPCaddress, RPCaddress2 = 'http://localhost:22000', 'http://localhost:22001' # use two different Quorum nodes for writing and reading  
# RPCaddress, RPCaddress2 = 'http://localhost:22001', 'http://localhost:22002' # crux dockerized, see https://github.com/blk-io/crux/blob/master/README.md#4-node-quorum-network-with-crux
RPCaddress, RPCaddress2 = 'http://localhost:8545', 'http://localhost:8545'  # orbita-center_parity-poa-playground; parity-deploy
# RPCaddress, RPCaddress2 = 'http://localhost:8545', 'http://localhost:8546'  # javahippie_geth-dev; use two different nodes for writing and reading  

# how many tx to send in send.py
NUMBER_OF_TRANSACTIONS = 20000

# obsolete now
# initially the contract was deployed manually with ./runscript.sh private-contract.js  
# And wait-for-something-to-happen was triggered by chain moving or not
# (which only works for raft & instantseal).
# Now obsolete because we can simply always deploy our own contract first,
# see deploy.py
# OLD:
# if consensus algorithm is Quorum raft, then --> True
# could be automated now ... from clienttype import clientType
# TODO: replace this constant by  clienttype CONSENSUS query 
# RAFT=False
# RAFT=True

## submit transaction via web3 or directly via RPC
ROUTE = "RPC"  # "web3" "RPC"
  
# parity's idiosyncracy:
# 'Time-unlocking is only supported in --geth compatibility mode.'
# see https://github.com/drandreaskrueger/chainhammer/blob/master/parity.md#run-14 for why and how
# so either --geth or unlockAccount() for each transaction, then make this True:
PARITY_UNLOCK_EACH_TRANSACTION=False

# to avoid the parity --geth switch, one could unlock parity already when starting, e.g.
# parity --unlock 0x39c6ad93dfb708143322d8bbf4c35734f6480249 --password /home/parity/password
# e.g. by manually editing the docker-compose.yml file after ./parity-deploy.sh --config aura --nodes 3
#  services: --> host1: --> command: --> add this: (address is in deployment/1/address.txt)
#    --unlock 0x39c6ad93dfb708143322d8bbf4c35734f6480249 --password /home/parity/password 
PARITY_ALREADY_UNLOCKED=False


# sorry, but time saving RPC optimisation makes no sense then anyways:
if PARITY_UNLOCK_EACH_TRANSACTION and ROUTE=="RPC":
    print ("Sorry, this parameter combination is not implemented:")
    print ('PARITY_UNLOCK_EACH_TRANSACTION and ROUTE=="RPC"')
    print ('change config.py, then restart.')
    exit(0)  


# gas given for .set(x) transaction 
# N.B.: must be different from (i.e. higher than) the eventually used gas in 
# a successful transaction; because difference is used as sign for a FAILED 
# transaction in the case of those clients which do not have a 
# 'transactionReceipt.status' field yet
GAS_FOR_SET_CALL = 90000 

# only for Quorum:
# set this to a list of public keys for privateFor-transactions, 
# or to None for public transactions 
PRIVATE_FOR = ["ROAZBWtSacxXQrOe3FGAqJDyJjFePR5ce4TSIzmJ0Bc="]
PRIVATE_FOR = None

# contract 7nodes example (probably this is 'SimpleStorage.sol'?)
EXAMPLE_ABI = [{"constant":True,"inputs":[],"name":"storedData","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"x","type":"uint256"}],"name":"set","outputs":[],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"get","outputs":[{"name":"retVal","type":"uint256"}],"payable":False,"type":"function"},{"inputs":[{"name":"initVal","type":"uint256"}],"type":"constructor"}];
EXAMPLE_BIN = "0x6060604052341561000f57600080fd5b604051602080610149833981016040528080519060200190919050505b806000819055505b505b610104806100456000396000f30060606040526000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680632a1afcd914605157806360fe47b11460775780636d4ce63c146097575b600080fd5b3415605b57600080fd5b606160bd565b6040518082815260200191505060405180910390f35b3415608157600080fd5b6095600480803590602001909190505060c3565b005b341560a157600080fd5b60a760ce565b6040518082815260200191505060405180910390f35b60005481565b806000819055505b50565b6000805490505b905600a165627a7a72305820d5851baab720bba574474de3d09dbeaabc674a15f4dd93b974908476542c23f00029"

# contract files:
FILE_CONTRACT_SOURCE  = "contract.sol"
FILE_CONTRACT_ABI     = "contract-abi.json"
FILE_CONTRACT_ADDRESS = "contract-address.json"

# account passphrase
FILE_PASSPHRASE = "account-passphrase.txt"

# DB file for traversing all blocks
DBFILE="allblocks.db"

if __name__ == '__main__':
    print ("Do not run this. Like you just did. Don't.")
    
    
