#!/usr/bin/env python3
"""
@summary: Which client type do we have? 
          quorum-raft/ibft OR energyweb OR parity OR geth OR ...

@version: v17 (19/June/2018)
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
    get a web3 object
    """
    w3 = Web3(HTTPProvider(RPCaddress, request_kwargs={'timeout': 120}))
    print ("web3 connection established, blockNumber =", w3.eth.blockNumber, end=", ")
    print ("node version string = ", w3.version.node)
    return w3


class Error(Exception):
    pass

class MethodNotExistentError(Error):
    pass


def curl_post(method, txParameters=None, RPCaddress=RPCaddress, ifPrint=False):
    """
    call Ethereum RPC functions that are still missing from web3.py 
    see
    https://github.com/jpmorganchase/quorum/issues/369#issuecomment-392240389
    """
    payload= {"jsonrpc" : "2.0",
               "method" : method,
               "id"     : 1}
    if txParameters:
        payload["params"] = [txParameters]
    headers = {'Content-type' : 'application/json'}
    response = requests.post(RPCaddress, json=payload, headers=headers)
    response_json = response.json()
    
    if ifPrint: 
        print('raw json response: {}'.format(response_json))
    
    if "error" in response_json:
        raise MethodNotExistentError()
    else:
        return response_json['result']
        

def clientType(w3):
    """
    queries several ethereum API endpoints, 
    to figure out which client type & consensus algorithm (e.g. RAFT)
    """

    consensus = "???"
    
    # Raft consensus?
    try:
        answer = curl_post(method="raft_role") # , ifPrint=True)
        if answer:
            consensus = "raft"
    except MethodNotExistentError:
        pass
    
        # IBFT consensus?    
        try:
            answer = curl_post(method="admin_nodeInfo")
            if 'istanbul' in answer.get('protocols', {}).keys():
                consensus = "istanbul"
        except:
            pass

    # Geth / Parity / Energy Web:
    nodeString = w3.version.node
    nodeType = nodeString.split("/")[0] 
    
    # Quorum pretends to be Geth - so how to distinguish vanillaGeth from QuorumGeth?
    nodeName = nodeType
    if consensus in ('raft', 'istanbul'):
        nodeName = "Quorum"
        
    if nodeName == "Energy Web":
        nodeType = "Parity"
        consensus = "PoA"  # TODO: study the answers of typical commands, can say more? 
    
    chainName="???"
    if nodeType=="Parity":
        try:
            chainName = curl_post(method="parity_chain") #  foundation, tobalaba
            if chainName=="foundation":
                consensus = "PoW"  # dangerous assumption, because some day that might actually change. For now fine. 
        except MethodNotExistentError:
            pass
    # TODO: Does geth also have a concept of chainName (e.g. for Morden/Ropsten/...)? How to query?
    
    return nodeName, nodeType, consensus, chainName
    

def test_clientType(w3):
    """
    test the above
    """
    nodeName, nodeType, consensus, chainName = clientType(w3)
    print ("nodeName: %s, nodeType: %s, consensus: %s, chainName: %s" % (nodeName, nodeType, consensus, chainName))


def justTryingOutDifferentThings():
    """
    perhaps these calls can help, or a combination thereof?
    also see 
    https://github.com/jpmorganchase/quorum/blob/3d91976f08074c1f7f605beaadf4b37783026d85/internal/web3ext/web3ext.go#L600-L671

    """
    for method in ("admin_nodeInfo", "net_version", "rpc_modules", 
                   "parity_chainId", "parity_chain", "parity_consensusCapability", 
                   "parity_nodeKind", "parity_versionInfo", ):
        print ("\n%s:" % method)
        try:
            pprint ( curl_post(method=method) )
        except:
            pass
        
        

if __name__ == '__main__':
    printVersions()
    w3 = start_web3connection(RPCaddress=RPCaddress) 

    test_clientType(w3)
    
    print()
    # justTryingOutDifferentThings()
    