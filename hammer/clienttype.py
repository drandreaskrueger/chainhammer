#!/usr/bin/env python3
"""
@summary: Which client type do we have? 
          quorum-raft/ibft OR energyweb OR parity OR geth OR ...

@version: v43 (16/December/2018)
@since:   29/May/2018
@organization: 
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates
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


# extend sys.path for imports:
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    
from hammer.config import RPCaddress



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
        
        
def clientTypeWarnings(nodeName, nodeType, consensus, networkId, chainName, chainId):
    if nodeName=="TestRPC":
        print ("WARN: TestRPC has odd timestamp units, check 'tps.timestampToSeconds()' for updates")
    if consensus=="raft":
        print ("WARN: raft consensus did report timestamps in nanoseconds. Is that still the case?")


def clientType(w3):
    """
    figure out which client (quorum, parity, geth, energyweb, etc.),
    which client type (fork of geth, or fork of parity),
    which consensus algorithm (e.g. RAFT, IBFT, aura, clique),
    and networkId, and chainId, and chainName.
    
    Sorry, very ugly, and probably faulty too, and for sure will break some day. 
    The fractions of the Ethereum world seem to have unsolved standardisation issues.
    
    See github issues
    * https://github.com/jpmorganchase/quorum/issues/505
    * https://github.com/jpmorganchase/quorum/issues/507
    * https://github.com/paritytech/parity-ethereum/issues/9432
    """

    consensus = "???"
    chainName = "???"
    networkId = -1
    chainId = -1
    
    try:
        answer = curl_post(method="net_version")
        networkId = int(answer) 
    except MethodNotExistentError:
        pass

    
    # How to detect raft consensus? 
    #        Unfortunately this fails with /quorum-example/7nodes 
    #        because they forgot to open the RPC api "raft"
    #        see issues 
    #
    #
    try:
        answer = curl_post(method="raft_role") # , ifPrint=True)
        if answer:
            consensus = "raft"
    except MethodNotExistentError:
        pass
    
        # IBFT consensus?
        # There is a specific answer, just in an unusual place; see issue
        #     https://github.com/jpmorganchase/quorum/issues/505
        try: 
            answer = curl_post(method="admin_nodeInfo")
            if 'istanbul' in answer.get('protocols', {}).keys():
                consensus = "istanbul"
        except:
            pass


    # Geth / Parity / Energy Web:
    nodeString = w3.version.node
    nodeName = nodeString.split("/")[0] 
    
    if nodeName == "Parity-Ethereum":
        nodeName = "Parity"

    # Quorum pretends to be Geth - so how to distinguish vanillaGeth from QuorumGeth?
    #  - see https://github.com/jpmorganchase/quorum/issues/507
    nodeType = nodeName    

    
    if consensus in ('raft', 'istanbul'):
        # TODO: Because raft RPC is not open in example (see above), this can 
        #       still not distinguish between vanilla geth, and quorum RAFT. 
        nodeName = "Quorum"
        
    if nodeName == "Energy Web":
        nodeType = "Parity"
        consensus = "PoA"  # Dangerous assumption. TODO: ... after they took care of the open issues, this gets easier. 


    if nodeType=="Parity":
        try:
            chainName = curl_post(method="parity_chain") #  foundation, tobalaba
            if chainName=="foundation":
                consensus = "PoW"  # dangerous assumption, because some day that might actually change. For now fine. 
        except MethodNotExistentError:
            pass
        try:
            answer = curl_post(method="parity_chainId")
            try:
                chainId = int(answer, 16)
            except TypeError:
                chainId = -1
        except MethodNotExistentError:
            pass

    
    if nodeName=="Geth":
        # TODO: This can still not distinguish between vanilla geth, and quorum RAFT. 
        try:
            answer = curl_post(method="admin_nodeInfo")
            
            answer_config = answer['protocols']['eth'].get('config', None)
            if answer_config:
                if "clique" in answer_config:
                    consensus="clique"
                if "ethash" in answer_config:
                    consensus="ethash"
                chainId = answer_config.get('chainId', None)
                
            # TODO: 
            # Does geth also have a concept of chainName (e.g. for Morden/Ropsten/...)? How to query?    
            # chainName = curl_post(method="net_version") #
            
        except MethodNotExistentError:
            pass
    
    clientTypeWarnings(nodeName, nodeType, consensus, networkId, chainName, chainId)
    
    return nodeName, nodeType, consensus, networkId, chainName, chainId
    

def run_clientType(w3):
    """
    test the above
    """
    nodeName, nodeType, consensus, networkId, chainName, chainId = clientType(w3)
    print ("nodeName: %s, nodeType: %s, consensus: %s, network: %s, chainName: %s, chainId: %s" % (nodeName, nodeType, consensus, networkId, chainName, chainId))


def justTryingOutDifferentThings(ifPrint=False):
    """
    perhaps these calls can help, or a combination thereof?
    also see 
    https://github.com/jpmorganchase/quorum/blob/3d91976f08074c1f7f605beaadf4b37783026d85/internal/web3ext/web3ext.go#L600-L671

    """
    for method in ("web3_clientVersion", "admin_nodeInfo", "net_version", "rpc_modules", 
                   "parity_chainId", "parity_chain", "parity_consensusCapability", 
                   "parity_nodeKind", "parity_versionInfo", "eth_chainId"):
        print ("\n%s:" % method)
    
        try:
            pprint ( curl_post(method=method, ifPrint=ifPrint) )
        except:
            pass
            

def simple_web3connection(RPCaddress):
    """
    get a web3 object. 
    simple, just for this demo here, 
    do not use elsewhere, instead use clienttools.start_web3connection
    """
    w3 = Web3(HTTPProvider(RPCaddress, request_kwargs={'timeout': 120}))
    print ("web3 connection established, blockNumber =", w3.eth.blockNumber, end=", ")
    print ("node version string = ", w3.version.node)
    return w3


if __name__ == '__main__':

    w3 = simple_web3connection(RPCaddress=RPCaddress) 

    run_clientType(w3)
    
    print()
    justTryingOutDifferentThings() # ifPrint=True)
    
