#!/usr/bin/env python3
"""
@summary: deploy contract; broken because Web3.py is broken. See DeployContractExample.py

@version: v08 (2/May/2018)
@since:   2/May/2018
@author:  https://github.com/drandreaskrueger
"""


################
## Dependencies:

import sys, time, random
from threading import Thread
from queue import Queue
from pprint import pprint

import requests # pip3 install requests

from web3 import Web3, HTTPProvider # pip3 install web3
from web3.utils.abi import filter_by_name, abi_to_signature
from web3.utils.encoding import pad_hex
from solc import compile_source # pip install py-solc

from send import unlockAccount, initialize
from config import RPCaddress, CONTRACT_SOURCE, CONTRACT_ABI, CONTRACT_ADDRESS

########################################################
## deploy example from
## http://web3py.readthedocs.io/en/stable/examples.html
########################################################

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)


def deploy_contract(w3, contract_interface):
    
    tx_hash = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
        ).deploy()

    address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
    return address


def wait_for_receipt(w3, tx_hash, poll_interval):
   while True:
       tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
       if tx_receipt:
         return tx_receipt
       time.sleep(poll_interval)


def deployContract(contractSource=CONTRACT_SOURCE):
    
    compiled_sol = compile_source_file(contractSource)
    contract_id, contract_interface = compiled_sol.popitem()
    # pprint (contract_interface); exit()
    
    address = deploy_contract(w3, contract_interface)
    print("Deployed {0} to: {1}\n".format(contract_id, address))

    pprint (txn_receipt)
    
    address = txn_receipt['contractAddress']
    with open(addressFile, "w") as f:
        f.write(address)
        
    return address



################
## basic tasks:
################



if __name__ == '__main__':

    # HTTP provider 
    # (TODO: try IPC provider, when quorum-outside-vagrant starts working)
    global w3
    w3 = Web3(HTTPProvider(RPCaddress, request_kwargs={'timeout': 120}))

    deployContract()
    