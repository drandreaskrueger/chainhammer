#!/usr/bin/env python3
"""
@summary: test Ethereum RPC = helps to identify the correct RPC-address

@version: v60 (26/October/2020)
@since:   26/October/2020
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates
"""

from pprint import pprint
import requests # pip3 install requests

print ("Start a network node, for example by:")
print ("    geth --rpc --dev")
input ("Press ENTER when ready")

RPCaddress =  'http://192.168.1.1:8545'
RPCaddress = 'http://wrongaddress:8545'
RPCaddress =    'http://localhost:8545'

# See e.g. https://eth.wiki/json-rpc/API#eth_blocknumber for methods
method, parameters = "eth_getBlockByNumber", ["0x0", False]
method, parameters = "eth_blockNumber", []
method, parameters = "eth_nonExistingMethod", []
method, parameters = "web3_clientVersion", []

payload= {"method"  : method,
          "params"  : parameters,
          "jsonrpc" : "2.0",
          "id"      : 1}
headers = {'Content-type' : 'application/json'}
print ("\nUsing '%s' to query RPC, with payload '%s'\n" % (RPCaddress, payload))

try:
    response = requests.post(RPCaddress, json=payload, headers=headers, timeout=5)
    
except Exception as e:
    print ("Bad: (%s) %s" % (type(e), e))
    print ("Try again...")
else:
    print ("response.status_code:", response.status_code)
    print ("response.text", response.text)
    error=response.json().get("error", None)
    if error:
        print ("Yes but only partial success, as we got an answer - but it says error='(%s) %s'" % (error['code'], error['message']))
    else:
        print ("method --> response.json()['result']:\n%s --> " % method, end="")
        pprint (response.json()['result'])
        print ("\nYes, full success. So this '%s' did answer. Great." % RPCaddress)
    
"""

# example output, in case of success:

Start a network node, for example by:
    geth --rpc --dev
Press ENTER when ready

Using 'http://localhost:8545' to query RPC, with payload '{'method': 'web3_clientVersion', 'params': [], 'jsonrpc': '2.0', 'id': 1}'

response.status_code: 200
response.text {"jsonrpc":"2.0","id":1,"result":"Geth/v1.9.6-stable/linux-amd64/go1.13.4"}

method --> response.json()['result']:
web3_clientVersion --> 'Geth/v1.9.6-stable/linux-amd64/go1.13.4'

Yes, full success. So this 'http://localhost:8545' did answer. Great.

"""