# taken from
# http://web3py.readthedocs.io/en/stable/contracts.html#contract-deployment-example
#
# then repaired:
# see issue 808 https://github.com/ethereum/web3.py/issues/808
# and extended
#
# and quorum-bugfixed, see
# https://github.com/ethereum/web3.py/issues/898#issuecomment-396701172

# tested with these versions:
#   web3 4.2.0
#   py-solc: 2.1.0
#   solc 0.4.23+commit.124ca40d.Linux.gpp
#   testrpc 1.3.4
#   python 3.5.3
# 
# does work      with TestRPCProvider()
# does work      with Energy Web//v1.12.0 (parity fork)
# now also works with Quorum 2.0.2 (fork of Geth/v1.7.2)

import json
import web3

from web3 import Web3, HTTPProvider
from solc import compile_source
from web3.contract import ConciseContract

# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.21;

contract Greeter {
    string public greeting;

    function Greeter() public {
        greeting = 'Hello';
    }

    function setGreeting(string _greeting) public {
        greeting = _greeting;
    }

    function greet() view public returns (string) {
        return greeting;
    }
}
'''

compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:Greeter']

# web3.py instance
# w3 = Web3(Web3.EthereumTesterProvider()) # wrong

# w3 = Web3(Web3.TestRPCProvider())                # works
# w3 = Web3(HTTPProvider('http://localhost:8545')) # works with Energy Web//v1.12.0 (account [0] must be unlocked)

# does NOT work with Quorum 2.0.2 --> Geth/v1.7.2
# Quorum = easiest way to run: as vagrant virtualbox
# step 1 https://github.com/jpmorganchase/quorum-examples#vagrant-usage
# step 2 https://github.com/jpmorganchase/quorum-examples/blob/master/examples/7nodes/README.md#7-nodes
w3 = Web3(HTTPProvider('http://localhost:22000'))  

nodeName = "Quorum"
if nodeName == "Quorum":
    # bugfix for quorum, see
    # https://github.com/ethereum/web3.py/issues/898#issuecomment-396701172
    from web3.middleware import geth_poa_middleware
    # inject the poa compatibility middleware to the innermost layer
    w3.middleware_stack.inject(geth_poa_middleware, layer=0)

# print client ID string:
print ("Node ID string:", w3.version.node)

# set pre-funded account as sender
w3.eth.defaultAccount = w3.eth.accounts[0]
print ("Sender's address", w3.eth.defaultAccount, "\n")

# Instantiate and deploy contract
Greeter = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Submit the transaction that deploys the contract
tx_hash = Greeter.constructor().transact()

print ("Tx submitted: ", w3.toHex(tx_hash))  # altered by me.

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# Create the contract instance with the newly-deployed address
greeter = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=contract_interface['abi'],
)

# Display the default greeting from the contract
print('Default contract greeting: {}'.format(
    greeter.functions.greet().call()
))

print('Setting the greeting to Nihao...')
tx_hash = greeter.functions.setGreeting('Nihao').transact()

# Wait for transaction to be mined...
w3.eth.waitForTransactionReceipt(tx_hash)

# Display the new greeting value
print('Updated contract greeting: {}'.format(
    greeter.functions.greet().call()
))

# When issuing a lot of reads, try this more concise reader:
reader = ConciseContract(greeter)
assert reader.greet() == "Nihao"
