
# OBSOLETE

is now tested part of [reproduce.md](reproduce.md).

## status of this file: 

* solved issue https://github.com/blk-io/crux/issues/39 but solution is not committed to their master yet
* preliminary results, one quick run: Fastest so far: 423-435 TPS !!!
* continue not before next week
* part of this then goes into the main [reproduce.md](reproduce.md), part into [quorum-IBFT.md](quorum-IBFT.md).

#### quorum IBFT network with 4 dockerized nodes
for details see [quorum-IBFT.md#crux-docker-4nodes](https://gitlab.com/electronDLT/chainhammer/blob/db3ae5da577d9b9d44c2879434993f3e0d44899f/quorum-IBFT.md#crux-docker-4nodes).

##### amazon AMI
use the same AWS image --> [reproduce.md#readymade-amazon-ami](reproduce.md#readymade-amazon-ami)

##### local build

Edit the given `blk-io/crux`, so that it builds a local docker container, instead of using `blkio10/quorum-crux:v1.0.0` from dockerhub:
```
git clone  https://github.com/blk-io/crux blk-io_crux
cd blk-io_crux/docker/quorum-crux/
cp docker-compose.yaml docker-compose-local.yaml
nano docker-compose-local.yaml 
```
Follow the instructions, so that it looks like this:
```
...
  node1: &quorum_crux_node
    # Pull image down from Docker Hub
    # image: blkio10/quorum-crux:v1.0.0
    # Uncomment the below, and comment out the above line to build the Docker images yourself
    image: blk.io/quorum/quorum-crux
    build:
      context: .
    container_name: quorum1
...
```

##### TPS-optimized network settings 

Edit the settings: Higher gas limit, larger txpool, blockperiod 1 second
```
sudo apt install jq
jq '.gasLimit = "0x1312D00"' istanbul-genesis.json > tmp && mv tmp istanbul-genesis.json

sed -i 's/PRIVATE_CONFIG/ARGS=$ARGS"--txpool.globalslots 20000 --txpool.globalqueue 20000 --istanbul.blockperiod 1 "\nPRIVATE_CONFIG/g' istanbul-start.sh 
```

then build the container, and start the network:
```
docker-compose -f docker-compose-local.yaml up --build
```

wait until you see something like

```
...
quorum1  | [*] Starting Crux nodes
quorum3  | [*] Starting Ethereum nodes
...
quorum1  | set +v
```

##### problems

(A) https://github.com/blk-io/crux/issues/39 [solved]


(B) (last week)  
something isn't working yet. Cannot connect to node, when installed on AWS:

```
geth attach http://localhost:22001
Fatal: Failed to start the JavaScript console: api modules: Post http://localhost:22001: EOF
```

no time for that now. 

not using quorum-crux for now; instead use plain vanilla `geth`.


(C)

new attempt. but something is really odd with this:

```
./deploy.py 

versions: web3 4.3.0, py-solc: 2.1.0, solc 0.4.24+commit.e67f0147.Linux.gpp, testrpc 1.3.4, python 3.5.3 (default, Jan 19 2017, 14:11:04) [GCC 6.3.0 20170118]
web3 connection established, blockNumber = 0, node version string =  Geth/v1.7.2-stable-3f1817ea/linux-amd64/go1.10.1
first account of node is 0xed9d02e382b34818e88B88a309c7fe71E65f419d, balance is 1000000000 Ether

nodeName: Quorum, nodeType: Geth, consensus: istanbul, network: 1, chainName: ???, chainId: -1

unlock:  True

tx_hash =  0x311ac387fd3069e81a9ad53e5bafc8ab8db8a1194b2eaa386a421b265d303381 --> waiting for receipt ...
Deployed. gasUsed=127173 contractAddress=0x1932c48b2bF8102Ba33B4A6B545C32236e342f34

.get(): 0

.set()

Traceback (most recent call last):
  File "./deploy.py", line 143, in <module>
    testMethods(myContract)
  File "./deploy.py", line 120, in testMethods
    tx_hash = w3.toHex( myContract.functions.set(answer + 1).transact() )
  File "/home/admin/electronDLT_chainhammer/py3eth/lib/python3.5/site-packages/web3/contract.py", line 1142, in transact
    **self.kwargs
  File "/home/admin/electronDLT_chainhammer/py3eth/lib/python3.5/site-packages/web3/contract.py", line 1438, in transact_with_contract_function
    txn_hash = web3.eth.sendTransaction(transact_transaction)
  File "/home/admin/electronDLT_chainhammer/py3eth/lib/python3.5/site-packages/web3/eth.py", line 262, in sendTransaction
    get_buffered_gas_estimate(self.web3, transaction),
  File "/home/admin/electronDLT_chainhammer/py3eth/lib/python3.5/site-packages/web3/utils/transactions.py", line 92, in get_buffered_gas_estimate
    "limit: {1}".format(gas_estimate, gas_limit)
    
ValueError: Contract does not appear to be deployable within the current network gas limits.  Estimated: 40029300. Current gas limit: 40019531
```

The tiny `.set()` function is running out of gas? Odd.  Why?

For now fixed with [hardcoding 90000 gas](https://gitlab.com/electronDLT/chainhammer/commit/c3ad840761cb769118a6b6074f9f4229c5b6eba8).


## results!!
preliminary, but see this post https://github.com/blk-io/crux/issues/39#issuecomment-422841365



