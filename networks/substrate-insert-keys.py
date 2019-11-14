#!/usr/bin/env python3
"""
@summary: insert pre-generated keys into N substrate nodes

@version: v60 (14/November/2019)
@since:   14/November/2019
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates
"""

import json, asyncio, websockets, sys, os
import websockets # pip3 install websockets

WS_URI = 'ws://127.0.0.1:9944/'

# CFG_PATH=os.path.join("..", "networks", "cfg")    # for development in IDE
CFG_PATH=os.path.join("networks", "cfg")          # for CLI usage


def async_call(command, params=[], callback=None, debug=False, ws_uri=WS_URI):
    """
    Websocket call. 
    Switch debug=True to see complete answer.
    """
    
    async def hello(uri):
        async with websockets.connect(uri) as websocket:
            message = dict()
            message["params"] = params
            message["method"] = command
            message["jsonrpc"], message["id"] = "2.0", 1
            if debug:
                print('Send: >>>> {}'.format(json.dumps(message, indent=4)))
                
            await websocket.send(json.dumps(message))
            data = await websocket.recv()
            
            if debug:
                print('Receive: <<<< {}'.format(json.dumps(json.loads(data), indent=4)))
                
            if callback is not None:
                callback(data)

    asyncio.get_event_loop().run_until_complete(hello(ws_uri))
    
    
def print_blocknumber(ws_uri=WS_URI):
    """
    First test of the above: current blocknumber = ?
    """
    print (ws_uri, end=" --> ")
    
    def deal_with_answer(data):
        datajson = json.loads(data)
        block_number = int(datajson['result']['number'], 16)
        print("block_number=", block_number)
    
    async_call(command="chain_getHeader", params=[], 
               callback=deal_with_answer, debug=False, ws_uri=ws_uri)


def all_block_numbers(N):
    """
    get block number for several node ports, on the same server
    """
    for i in range(N):
        port=9944+i
        print_blocknumber('ws://127.0.0.1:%d/' % port)
        
        
def insertKey(keytype, suri, pubkey, ws_uri):
    """
    call author.insertKey(keytype,suri,pubkey)
    handle errors
    """
    
    params=[keytype, suri, pubkey]
    
    def deal_with_answer(data):
        datajson = json.loads(data)
        error=datajson.get("error", None)
        if error:
            print ("ERROR(%s).message='%s'" % (error["code"],error["message"]))
        else:
            result = datajson['result']
            print("result=%s" % result)
    
    async_call(command="author_insertKey", params=params, 
               callback=deal_with_answer, debug=False, ws_uri=ws_uri)
    

def insertKeys(seedphrases, pubkeys, ws_start_uri=WS_URI):
    """
    for many nodes (each one with its unique suri):
        for babe,gran:
            call author.insertKey(babe or gran, suri, pubkey) 
    """
    ws_start_port = ws_start_uri.split(":")[2].replace("/","")
    ws_uri_template = ws_start_uri.replace(ws_start_port, "%d")
    ws_start_port = int(ws_start_port)
    
    print ("Insert all %d keys. Begin with uri: %s\n" %(2*len(pubkeys), 
                                                      ws_uri_template % ws_start_port))  
    for i, seed in enumerate(seedphrases):
        pk=pubkeys[i]
        port = ws_start_port+i
        ws_uri = ws_uri_template % port
        print (ws_uri, " --> ")
        for keytype in ("babe", "gran"):
            print ("insertKey(%s, %s, %s, %s)" % (keytype, seed[:20]+"...", pk[keytype][:12]+"...", "...:%d" % port), end= " --> ")
            insertKey(keytype, seed, pk[keytype], ws_uri)
        
    print ("\nDone.")
    

def load_seeds(N):
    """
    load the N files, with one line per file
    """
    seedphrases=[]
    for i in range(1, N+1):
        filename = os.path.join(CFG_PATH, "seed%d.secret" % i)
        with open(filename, "r") as f:
            seedphrases.append(f.readline().strip())
    return seedphrases

def load_pubkeys(N):
    """
    load the N files, with two lines per file
    """
    pubkeys=[]
    for i in range(1, N+1):
        filename = os.path.join(CFG_PATH, "seed%d.babegran" % i)
        with open(filename, "r") as f:
            pubkeys.append({"babe": f.readline().strip(),
                            "gran": f.readline().strip()})
    return pubkeys
            

def CLI_arg():
    if len(sys.argv)<2:
        print ("give number of nodes as integer arg please")
        exit()
    return int(sys.argv[1])


if __name__ == '__main__':
    
    N=CLI_arg()
    print ("Connection test to %d nodes:" % N)
    all_block_numbers(N)

    print ()    
    seedphrases=load_seeds(N)
    pubkeys=load_pubkeys(N)
    # print (seedphrases); print (pubkeys)
    insertKeys(seedphrases, pubkeys)
    
    
    