from clienttype import *
from config import RPCaddress
import web3

global w3
w3=simple_web3connection(RPCaddress)

def test_simple_web3connection():
    global w3
    assert type(w3) == web3.main.Web3
    
def test_curl_post():
    method="eth_blockNumber"
    answer = curl_post(method, ifPrint=True)
    print (method, answer)
    assert type(answer)==type("") # that the answer (blocknumber) is a string


import pytest

def test_curl_post_MethodNotExistentError():
    method="eth_thisMethodDoesNotExist"
    with pytest.raises(MethodNotExistentError):
        answer = curl_post(method, ifPrint=True)
        print (answer)

def test_clientType():
    answer = clientType(w3)
    print (answer)
    assert len(answer) == 6