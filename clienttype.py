#!/usr/bin/env python3
"""
@summary: Which client type do we have? 
          quorum-raft/ibft OR energyweb OR parity OR geth OR ...

@version: v14 (29/May/2018)
@since:   29/May/2018
@organization: electron.org.uk
@author:  https://github.com/drandreaskrueger
@see: https://gitlab.com/electronDLT/chainhammer for updates
"""


################
## Dependencies:

import json
from pprint import pprint
import requests # pip3 install requests

try:
    from web3 import Web3, HTTPProvider # pip3 install web3
except:
    print ("Dependencies unavailable. Start virtualenv first!")
    exit()

from config import RPCaddress, printVersions


def start_web3connection(RPCaddress=None):
    """
    get a global web3 object
    """
    global w3
    w3 = Web3(HTTPProvider(RPCaddress, request_kwargs={'timeout': 120}))
    print ("web3 connection established, blockNumber =", w3.eth.blockNumber, end=", ")
    print ("node version string = ", w3.version.node)
    return w3


class Error(Exception):
    pass

class MethodNotExistentError(Error):
    pass


def curl_post(method, txParameters=[], RPCaddress=RPCaddress, ifPrint=False):
    """
    call Ethereum RPC functions that are still missing from web3.py 
    see
    https://github.com/jpmorganchase/quorum/issues/369#issuecomment-392240389
    """
    payload= {"jsonrpc" : "2.0",
               "method" : method,
               "params" : [txParameters],
               "id"     : 1}
    headers = {'Content-type' : 'application/json'}
    response = requests.post(RPCaddress, json=payload, headers=headers)
    response_json = response.json()
    
    if ifPrint: 
        print('raw json response: {}'.format(response_json))
    
    if "error" in response_json:
        raise MethodNotExistentError()
    else:
        return response_json['result']
        

def clientType():
    """
    queries several ethereum API endpoints, 
    to figure out which client type & consensus algorithm (e.g. RAFT)
    """
    
    # Raft consensus?
    try:
        answer = curl_post(method="raft_role") # , ifPrint=True)
        if answer:
            consensus = "raft"
    except MethodNotExistentError:
        consensus = "???"

    # IBFT consensus?
    ## TODO: what is the best analogous call to the above?

    # Geth / Parity / Energy Web:
    nodeString = w3.version.node
    nodeType = nodeString.split("/")[0] 
    
    # Quorum pretends to be Geth - so how to distinguish vanillaGeth from QuorumGeth?
    ## TODO, candidates: 
    ## 
    ## admin_nodeInfo --> protocols --> istanbul 
    ## (but unfortunately, when "raft", that pretends to be  --> protocols --> eth)  
    
    return nodeType, consensus
    

def test_clientType():
    """
    test the above
    """
    nodeType, RAFT = clientType()
    print ("nodeType: %s, consensus: %s" % (nodeType, RAFT))


def justTryingOutDifferentThings():
    """
    perhaps these calls can help, or a combination thereof?
    also see 
    https://github.com/jpmorganchase/quorum/blob/3d91976f08074c1f7f605beaadf4b37783026d85/internal/web3ext/web3ext.go#L600-L671

    """
    for method in ("admin_nodeInfo", "net_version", "rpc_modules"):
        print ("\n%s:" % method)
        pprint ( curl_post(method=method) )
        
        

if __name__ == '__main__':
    printVersions()
    start_web3connection(RPCaddress=RPCaddress) 

    test_clientType()
    
    print()
    justTryingOutDifferentThings()
    