#!/usr/bin/env python

# WS client example for old Python versions (using python 3.5)
# from https://websockets.readthedocs.io/en/stable/intro.html#python-lt-36

import asyncio
import websockets
import json

ID=1

def methodcall2text(method, params):
    global ID
    request = {
        "jsonrpc": "2.0",
        "method": method,
        "params": [] if params is None else params,
        "id": ID
    }
    ID += 1
    data=json.dumps(request)
    return data
    

@asyncio.coroutine
def hello(method="system_version", data=None):
    websocket = yield from websockets.connect('ws://127.0.0.1:11000/')
    
    try:
        payload = methodcall2text(method, data)
        yield from websocket.send(payload)
        print("> {}".format(payload))

        answer = yield from websocket.recv()
        print("< {}".format(answer))

    finally:
        yield from websocket.close()


asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_until_complete(hello(method="chain_getBlockHash", data=[0]))

'''
> {"id": 1, "jsonrpc": "2.0", "method": "system_version", "params": []}
< {"jsonrpc":"2.0","result":"2.0.0","id":1}

> {"id": 2, "jsonrpc": "2.0", "method": "chain_getBlockHash", "params": [0]}
< {"jsonrpc":"2.0","result":"0x49e81f64bf363aeb2224a9d74a6c88a9d3fa63948f1e1878a06d7fd934768a68","id":2}
'''