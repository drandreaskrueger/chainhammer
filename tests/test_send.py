import os
from pprint import pprint
from web3.utils import datatypes

from config import RPCaddress, FILE_CONTRACT_SOURCE

from clienttools import web3connection
answer = web3connection(RPCaddress=RPCaddress)
global w3, NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID 
w3, chainInfos  = answer
NODENAME, NODETYPE, CONSENSUS, NETWORKID, CHAINNAME, CHAINID = chainInfos

import send
import deploy
deploy.w3 = send.w3 = w3

# path for the contract sourcecode file
# unfortunately path if different depending on how py.test is called
path=os.path.abspath(os.curdir)
if os.path.split(path)[-1]=="tests":
    os.chdir("..") 

# fixture: create a contract that every test here can be using
_,interface,address = deploy.contract_CompileDeploySave(FILE_CONTRACT_SOURCE)
contract = deploy.contractObject(address, interface["abi"])
abi = interface["abi"]
 

def test_initialize_fromAddress():
    contract = send.initialize_fromAddress()
    print (contract)
    assert ("%s" % contract).startswith("<web3.utils.datatypes.Contract object")


def test_contract_set_via_web3():
    arg = 1000
    stored = send.try_contract_set_via_web3(contract, arg)
    assert arg == stored # hmmm ... don't we have to wait for the receipt?


def test_contract_method_ID():
    methodname = "get"
    answer = send.contract_method_ID(methodname, abi)
    print (answer)
    assert answer == "0x6d4ce63c"


def test_argument_encoding():
    method_ID = send.contract_method_ID("set", abi) # TODO: make this "set" flexible for any method name
    data = send.argument_encoding(method_ID, arg=42)
    print (data)
    assert data == "0x60fe47b1000000000000000000000000000000000000000000000000000000000000002a"
    
    
def test_contract_set_via_RPC():
    arg = 1001
    tx = send.contract_set_via_RPC(contract, arg=arg)
    print (tx)
    assert tx.startswith("0x")
    stored = contract.functions.get().call()
    assert arg == stored


# unready

