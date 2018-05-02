# http://web3py.readthedocs.io/en/stable/examples.html
# as on 2018 May 2nd
# then improved until no more errors


# problem was (probably): 'stable' manual but 'latest' library




import sys
import time
import pprint

from web3.providers.eth_tester import EthereumTesterProvider
from web3 import Web3
from solc import compile_source

from web3 import Web3, HTTPProvider, __version__ as web3version # pip3 install web3
from solc import get_solc_version
from eth_tester import __version__ as ethtesterversion
print ("versions: web3 %s, solc %s, eth_tester %s, python %s" % (web3version, get_solc_version(), ethtesterversion, sys.version.replace("\n", "")))

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()

   return compile_source(source)


def wait_for_receipt(w3, tx_hash, poll_interval=0.5):
   while True:
       tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
       if tx_receipt:
         return tx_receipt
       time.sleep(poll_interval)


def deploy_contract(w3, contract_interface):
    
    transaction = {"from": w3.eth.coinbase,
                   "gas" : 100000}
    
    # tx_hash = w3.eth.contract(
        # bytecode=contract_interface['bin']).deploy() # this failed
        # abi=contract_interface['abi'],
        # bytecode=contract_interface['bin']).deploy(transaction=transaction)
    
    contract = w3.eth.contract(bytecode = contract_interface['bin'], 
                               abi = contract_interface['abi'])
    
    # tx_hash = contract.deploy(transaction=transaction)
    tx_hash = contract.constructor.transact(transaction=transaction) # AttributeError: 'function' object has no attribute 'transact'
        
    receipt = wait_for_receipt(w3, tx_hash)
    address = receipt['contractAddress']
    return address


w3 = Web3(EthereumTesterProvider())
# w3 = Web3(HTTPProvider('http://localhost:22000'))

contract_source_path = 'contract.sol'
compiled_sol = compile_source_file('contract.sol')

contract_id, contract_interface = compiled_sol.popitem()

address = deploy_contract(w3, contract_interface)
print("Deployed {0} to: {1}\n".format(contract_id, address))


