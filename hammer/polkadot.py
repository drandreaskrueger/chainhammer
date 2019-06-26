#!/usr/bin/env python

# WS client example for old Python versions (using python 3.5)
# from https://websockets.readthedocs.io/en/stable/intro.html#python-lt-36

import asyncio
import websockets

@asyncio.coroutine
def hello():
    websocket = yield from websockets.connect('ws://127.0.0.1:11000/')
    
    try:
        name="client_version"
        yield from websocket.send(name)
        print("> {}".format(name))

        greeting = yield from websocket.recv()
        print("< {}".format(greeting))

    finally:
        yield from websocket.close()

asyncio.get_event_loop().run_until_complete(hello())

''' 
> client.version()
< {"jsonrpc":"2.0","error":{"code":-32700,"message":"Parse error"},"id":null}

> client.version
< {"jsonrpc":"2.0","error":{"code":-32700,"message":"Parse error"},"id":null}

> client_version
< {"jsonrpc":"2.0","error":{"code":-32700,"message":"Parse error"},"id":null}
'''