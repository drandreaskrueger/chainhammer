# taken from
# http://web3py.readthedocs.io/en/latest/contracts.html#contract-deployment-example
# then updated:
# was broken, see issue 808 https://github.com/ethereum/web3.py/issues/808
# fixed, see https://github.com/ethereum/web3.py/issues/808#issuecomment-386014138

import json
import web3

from web3 import Web3
from solc import compile_source
from web3.contract import ConciseContract

from config import printVersions; printVersions() # added by me

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
# w3 = Web3(Web3.EthereumTesterProvider()) # bug, see https://github.com/ethereum/web3.py/issues/808#issuecomment-386014138
w3 = Web3(Web3.TestRPCProvider()) # added by me

# set pre-funded account as sender
w3.eth.defaultAccount = w3.eth.accounts[0]

# Instantiate and deploy contract
Greeter = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Submit the transaction that deploys the contract
tx_hash = Greeter.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print ( "Deployed. gasUsed={gasUsed} contractAddress={contractAddress}".format(**tx_receipt) ) # added by me 

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





