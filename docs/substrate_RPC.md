# substrate via RPC 
Following this hint https://github.com/paritytech/substrate/issues/4103#issuecomment-555044927 and using my new substrate node

    substrate-node-template/target/release/substrate-node-template --dev

that I had learned to create in the tutorial [substrate_creating-your-first-chain.md](substrate_creating-your-first-chain.md).

Now following the [blog page](https://www.shawntabrizi.com/substrate/querying-substrate-storage-via-rpc/) but on localhost. First on `https://localhost:9933/` I got the error: `curl: (35) error:140770FC:SSL routines:SSL23_GET_SERVER_HELLO:unknown protocol` but with `http://` instead of `https://` it then worked:

     curl -H "Content-Type: application/json" -d '{"id":1, "jsonrpc":"2.0", "method": "state_getMetadata"}' http://127.0.0.1:9933/ | jq

we then need the SCALE codec, so:

    cd chainhammer
    source env/bin/activate
    cd networks/repos
    git clone https://github.com/polkascan/py-scale-codec polkascan_py-scale-codec
    cd polkascan_py-scale-codec
    python ./setup.py install

see substrate_RPC_testing.py (and substrate_RPC-flaw.py) for more details.

and -hooray- there is a Python library, for some of the RPC calls

    cd .. 
    git clone https://github.com/polkascan/py-substrate-interface.git polkascan_py-substrate-interface
    cd polkascan_py-substrate-interface 
    python ./setup.py install

(both are now getting installed via `scripts/install-virtualenv.sh`)

I have tried out most functions in polkascan's `py-substrate-interface`, see `substrateinterface_testing.py`. Then I have come up with one feature request 
[psi#2](https://github.com/polkascan/py-substrate-interface/issues/2) and when no answer, I solved it myself in pull request [psi#4](https://github.com/polkascan/py-substrate-interface/pull/4); and asked for a working  example how to use one of their functions [psi#3](https://github.com/polkascan/py-substrate-interface/issues/3) because they have no unittests yet.


## issues
* [pspsc#4](https://github.com/polkascan/py-scale-codec/issues/4) self.contains_transaction: bool = False ^ SyntaxError: invalid syntax
* [sdh#11](https://github.com/substrate-developer-hub/substrate-node-template/issues/11) using canonical Python requests --> {"code":-32700,"message":"Parse error"}
* [ipxx#34](https://github.com/ifduyue/python-xxhash/issues/34) 128 bits ?
* [psi#2](https://github.com/polkascan/py-substrate-interface/issues/2) (FR) let the function do the xxhash'ing of the storage key name
* [psi#3](https://github.com/polkascan/py-substrate-interface/issues/3) example for get_storage(module, function, params) please
* [psi#4](https://github.com/polkascan/py-substrate-interface/pull/4) allow human readable key name: get_storage_by_key(storage_key_name)
* [psi#13](https://github.com/polkascan/py-substrate-interface/issues/13) get_runtime_events() --> RemainingScaleBytesNotEmptyException

