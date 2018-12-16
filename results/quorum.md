N.B.: Going to be redone, when repeated in the cloud (all experiments here were on a local desktop). For that we'd need this solved: [BC#51](https://github.com/blk-io/crux/issues/51) to be able to run in docker (not vagrant virtualbox).

# [chainhammer](../README.md): quorum
Quorum raft TPS measurements. Uses the [quorum-examples --> 7nodes](https://github.com/jpmorganchase/quorum-examples/blob/master/examples/7nodes/README.md) example.

## TOC
1. general infos on quorum
1. initialize 7nodes quorum-example
1. virtualenv; start listener; start hammering
1. blocking,  multithreaded 1, multithreaded 2, 
1. example output
1. chainreader
1. faster
1. much later repeat
1. suggestions please
1. IBFT = Istanbul BFT
1. [issues raised](issues-raised)
1. alternative: dockerized quorum nodes
1. credits

## general infos 


about quorum

* there are (at least) two Quorum variants now:
  * (orig) by EEA/jpmc https://github.com/jpmorganchase/quorum 
  * (fork) by ConsenSys https://github.com/ConsenSys/quorum
* integrated whole networks:
  * 7nodes `constellation` (vagrant virtualbox) https://github.com/jpmorganchase/quorum-examples
  * 7nodes `crux` (vagrant virtualbox) https://github.com/blk-io/quorum-examples
  * 4 nodes `crux` (docker) https://github.com/blk-io/crux/tree/master/docker/quorum-crux

about this benchmarking

* raft consensus: this document here
* Istanbul BFT consensus: [quorum-IBFT.md](quorum-IBFT.md)

## initialize 7nodes

edit `v.memory = 2048` into `v.memory = 4096` (see [#85](https://github.com/jpmorganchase/quorum-examples/issues/85)):
```
git clone https://github.com/jpmorganchase/quorum-examples
cd quorum-examples
nano Vagrantfile
```

```
vagrant up
vagrant status
vagrant ssh
```

```
cd quorum-examples/7nodes
./raft-init.sh
./raft-start.sh
sleep 3
ps aux | grep geth

./runscript.sh script1.js
```
if that says sth like

> Contract transaction send: TransactionHash: 0x00594... waiting to be mined...  
> true

then we now have a block 1 transaction 0 which contains a simple set()/get() smart contract, which we will later fire our transactions at.

see [send.py](../hammer/send.py) --> ` initialize(contractTx_blockNumber=1, contractTx_transactionIndex=0)`

## virtualenv 
for py3 dependencies, mostly ethereum 
```
virtualenv -p python3 py3eth
source env/bin/activate
python3 -m pip install --upgrade pip==9.0.3
pip3 install --upgrade py-solc==2.1.0 web3==4.3.0 web3[tester]==4.3.0 rlp==0.6.0 eth-testrpc==1.3.4 requests 
```
see [hints from the Web3.py team](https://github.com/ethereum/web3.py/issues/808#issuecomment-386014138)

## start listener

```
python tps.py
```

## start hammering

### blocking
```
python send.py
```

Initially could see only 12-15 tps; eventually (raft, non-private contract) about 100 TPS average.

### multithreaded 1

you must kill (`CTRL-C`), and restart the listener, then:

```
python send.py threaded1
```
 
The best rate that I have seen was 146 TPS, as average over 1000 transactions.


### multithreaded 2
not a new thread per each of the `N` transaction but a queue with `M` multithreaded workers. 

```
python send.py threaded2 23
```

see [log.md](log.md) for details, and the sweet spot `M=23`

Best average rate: 177 TPS.

## example output

```
Block  4682  - waiting for something to happen

starting timer, at block 4683 which has  1  transactions; at timecode 1524133452.88
block 4683 | new #TX   4 /   73 ms =  54.5 TPS_current | total: #TX    5 /  0.1 s =  72.6 TPS_average
block 4685 | new #TX  23 /  250 ms =  91.7 TPS_current | total: #TX   28 /  0.5 s =  57.3 TPS_average
block 4690 | new #TX  22 /  504 ms =  43.6 TPS_current | total: #TX   50 /  0.9 s =  55.0 TPS_average
block 4697 | new #TX  39 /  446 ms =  87.4 TPS_current | total: #TX   89 /  1.4 s =  62.6 TPS_average
block 4703 | new #TX  15 /  464 ms =  32.3 TPS_current | total: #TX  104 /  1.8 s =  56.5 TPS_average
block 4708 | new #TX  32 /  332 ms =  96.3 TPS_current | total: #TX  136 /  2.3 s =  60.0 TPS_average
block 4714 | new #TX  39 /  305 ms = 127.8 TPS_current | total: #TX  175 /  2.7 s =  65.0 TPS_average
block 4720 | new #TX  23 /  695 ms =  33.1 TPS_current | total: #TX  198 /  3.2 s =  62.8 TPS_average
block 4727 | new #TX  36 /  238 ms = 150.8 TPS_current | total: #TX  234 /  3.6 s =  64.9 TPS_average
block 4731 | new #TX  74 /  476 ms = 155.1 TPS_current | total: #TX  308 /  4.0 s =  76.2 TPS_average
block 4740 | new #TX  28 /  591 ms =  47.3 TPS_current | total: #TX  336 /  4.5 s =  75.1 TPS_average
block 4745 | new #TX  22 /  444 ms =  49.5 TPS_current | total: #TX  358 /  4.9 s =  72.5 TPS_average
block 4751 | new #TX  48 /  498 ms =  96.2 TPS_current | total: #TX  406 /  5.4 s =  75.8 TPS_average
block 4757 | new #TX   6 /  150 ms =  39.8 TPS_current | total: #TX  412 /  5.8 s =  71.4 TPS_average
block 4760 | new #TX  66 /  292 ms = 225.5 TPS_current | total: #TX  478 /  6.2 s =  77.2 TPS_average
block 4762 | new #TX  18 /  356 ms =  50.5 TPS_current | total: #TX  496 /  6.6 s =  75.1 TPS_average
block 4767 | new #TX  29 /  300 ms =  96.7 TPS_current | total: #TX  525 /  7.0 s =  74.9 TPS_average
block 4772 | new #TX  62 /  699 ms =  88.6 TPS_current | total: #TX  587 /  7.5 s =  78.2 TPS_average
block 4782 | new #TX  28 /  700 ms =  40.0 TPS_current | total: #TX  615 /  8.1 s =  76.3 TPS_average
block 4791 | new #TX  55 /  501 ms = 109.6 TPS_current | total: #TX  670 /  8.5 s =  78.8 TPS_average
block 4800 | new #TX  22 /  255 ms =  86.0 TPS_current | total: #TX  692 /  9.0 s =  77.0 TPS_average
block 4803 | new #TX  42 /  392 ms = 107.0 TPS_current | total: #TX  734 /  9.4 s =  78.0 TPS_average
block 4810 | new #TX  30 /  500 ms =  59.9 TPS_current | total: #TX  764 /  9.9 s =  76.9 TPS_average
block 4816 | new #TX 119 /  608 ms = 195.6 TPS_current | total: #TX  883 / 10.4 s =  85.2 TPS_average
block 4822 | new #TX 117 /  358 ms = 326.1 TPS_current | total: #TX 1000 / 10.8 s =  92.9 TPS_average
```

### chainreader
* Quorum, raft consensus
* submitted 1000 transactions, multi-threaded with 23 workers
* the image shows the third such experiment on a newly started [quorum-examples/7nodes](https://github.com/jpmorganchase/quorum-examples/tree/master/examples/7nodes) network
* average TPS around 160 TPS, about 20 blocks per second

![chainreader/img/quorum_tps-bt-bs-gas_blks242-357.png](../reader/img/quorum_tps-bt-bs-gas_blks242-357.png)


## faster

See [log.md](log.md) for what I have tried to get this faster.

### Much later repeat

With newest chainhammer code (version [v24](https://github.com/drandreaskrueger/chainhammer/commit/69407bab63ca56fb62bae736c9cf3e6a7c32c6c0)), 
and with 10 multithreading workers, 
and with RPC calls instead of web3.contract calls, 
and with 7nodes in the standard constellation version of the [quorum-examples-->raft](https://github.com/jpmorganchase/quorum-examples),
we are seeing around ~200 TPS now for raft consensus:

```
./tps.py 

versions: web3 4.3.0, py-solc: 2.1.0, solc 0.4.23+commit.124ca40d.Linux.gpp, testrpc 1.3.4, python 3.5.3 (default, Jan 19 2017, 14:11:04) [GCC 6.3.0 20170118]
web3 connection established, blockNumber = 1215, node version string =  Geth/v1.7.2-stable-99a83767/linux-amd64/go1.9.3
first account of node is 0x0fBDc686b912d7722dc86510934589E0AAf3b55A, balance is 1000000000 Ether
nodeName: Quorum, nodeType: Geth, consensus: raft, network: 10, chainName: ???, chainId: -1
Block  1215  - waiting for something to happen
(filedate 1536069903) last contract address: 0x055a8A01cbaCa453B7a6f1BBFfa9233710452dcd
(filedate 1536069957) new contract address: 0x3358609DbD8718d8d7788E2971696a8d94a905aa
blocknumber_start_here = 1216
starting timer, at block 1216 which has  1  transactions; at timecode 22593.923337597

block 1216 | new #TX  10 /  699 ms =  14.3 TPS_current | total: #TX   11 /  0.7 s =  16.3 TPS_average
block 1219 | new #TX  52 /  213 ms = 244.5 TPS_current | total: #TX   63 /  1.1 s =  56.2 TPS_average
block 1223 | new #TX  75 /  438 ms = 171.3 TPS_current | total: #TX  138 /  1.5 s =  89.1 TPS_average
block 1231 | new #TX  51 /  204 ms = 250.6 TPS_current | total: #TX  189 /  2.0 s =  95.0 TPS_average
[...]
block 2418 | new #TX  80 /  688 ms = 116.3 TPS_current | total: #TX 17181 / 91.7 s = 187.4 TPS_average
block 2428 | new #TX 103 /  464 ms = 222.1 TPS_current | total: #TX 17284 / 92.1 s = 187.6 TPS_average
block 2434 | new #TX 136 /  932 ms = 145.9 TPS_current | total: #TX 17420 / 92.8 s = 187.7 TPS_average
block 2448 | new #TX 130 /  300 ms = 433.5 TPS_current | total: #TX 17550 / 93.2 s = 188.2 TPS_average
block 2453 | new #TX 2451 / 10706 ms = 228.9 TPS_current | total: #TX 20001 / 97.0 s = 206.1 TPS_average
```

### suggestions please
how can I speed this up?

* see [jpmsam suggestions April 18th](https://github.com/jpmorganchase/quorum/issues/346#issuecomment-382523147)
  * run on host machine, not in vagrant VB - implemented, but [crashes](https://github.com/jpmorganchase/quorum/issues/352)
  * direct RPC communication not via web3 - implemented, gives a slight improvement
  * [eth_sendTransactionAsync](https://www.google.co.uk/search?q="eth_sendTransactionAsync") - not implemented yet, might also not be generally applicable in all situations, right?
* replace `constellation` by [Crux](https://github.com/blk-io/crux) ???


## IBFT = Istanbul BFT
All of the above was done with the "Raft Consensus Algorithm".

**Next I would be switching to *"Istanbul Byzantine Fault Tolerant" (IBFT)* ** Consensus Algorithm.

Differences to the raft chainhammer code (already solved, to benchmark the [Tobalaba](tobalaba.md) EnergyWebClient):

* the smart contract deployment transaction cannot reliably be found in block 0; instead 
  * we reimplemented `script1.js` into a real programming language, which is allowed to write to file --> `deploy.py`
* 'raft' is producing no empty blocks, so the trigger for ["waiting for something to happen"](https://github.com/drandreaskrueger/chainhammer/blob/ca97cf5de66df03b26e3bf28f2a0ca9a621cc781/tps.py#L108-110) needed be a different one than blocks moving forwards; it is now just waiting for that `contract-address.json` file to be updated.

--> benchmarking IBFT should be simple, and straightforward. Let's see:

in 7 nodes quorum-examples:
```
cd quorum-examples/7nodes/
./istanbul-init.sh 
./istanbul-start.sh 
tail -f qdata/logs/1.log 
```

in chainhammer:
`config.py`: 
```
RPCaddress, RPCaddress2 = 'http://localhost:22000', 'http://localhost:22001'
RAFT=False
```
terminal 1:
```
source env/bin/activate
./tps.py
```
terminal 2:
```
source env/bin/activate
./deploy.py notest; ./send.py threaded2 23
```

Does not work yet, as contract deployment seems to be slightly different in "Quorum" (Geth) than in "Energy Web" (Parity).


## issues raised
while exploring this, I ran into issues with Quorum(Q) and QuorumExamples(QE):

* [Q #322](https://github.com/jpmorganchase/quorum/issues/322) **tests failing (v2.0.2)** 
  * non-failing tests are ... nice to have ;-)
* [Q #346](https://github.com/jpmorganchase/quorum/issues/346) **~90 tps?** 
  * ongoing discussion!
* [Q #351](https://github.com/jpmorganchase/quorum/issues/351) **version mismatch 2.0.2 --> 2.0.1** 
  * tiny issue only
* [Q #352](https://github.com/jpmorganchase/quorum/issues/352) **panic: runtime error: invalid memory address or nil pointer dereference** 
  * needs fixing, before I can continue!
* [QE #85](https://github.com/jpmorganchase/quorum-examples/issues/85) **7nodes node crashing - fatal error: runtime: out of memory**
  * Increase memory in vagrant config file
* [QE #86](https://github.com/jpmorganchase/quorum-examples/issues/86) **7nodes: some nodes with web3.eth.accounts==[ ]** 
  * nice to have
* [QE #87](https://github.com/jpmorganchase/quorum-examples/issues/87) **7nodes: private.set(3) fails with a 500 Internal Server Error when done from node 7**
  * was only: lack of good error message
* [QE #90](https://github.com/jpmorganchase/quorum-examples/issues/90) **2 recipient keys in `privateFor` - not working???** 
  * *"its not currently possible to add a new participant to an existing private contract. It's one of the enhancements that we have in our backlog."*
* [QE PR #93](https://github.com/jpmorganchase/quorum-examples/pull/93) **initialize JSRE var with deployed contract, and script2.js to deploy privateFor 2 recipients**
* [Q #369](https://github.com/jpmorganchase/quorum/issues/369) FR: new API endpoint/answer
* [Web3.py #808](https://github.com/ethereum/web3.py/issues/808) --> solved
* [Web3.py #898](https://github.com/ethereum/web3.py/issues/898) --> solved
* [Q #505](https://github.com/jpmorganchase/quorum/issues/505) **please consider to return more standardized answers about consensus algorithms**
* [BQE #33](https://github.com/blk-io/crux/issues/33) Server does not implement chimera.ClientServer (missing Delete method)
* [Q #507](https://github.com/jpmorganchase/quorum/issues/507) `Quorum/v2.1.0-stable-159d813f/linux-amd64/go1.9.3`
* [QE#121](https://github.com/jpmorganchase/quorum-examples/issues/121) --rpcapi ...,raft
* [BC#51](https://github.com/blk-io/crux/issues/51) (FR) dockerized with raft consensus not IBFT 

## alternative: dockerized quorum nodes
Always used the 7nodes example as described above, but there is also https://github.com/ConsenSys/quorum-docker-Nnodes = Run a bunch of Quorum nodes, each in a separate Docker container. Untested.

# credits
Please credit this as:

> benchmarking scripts "chainhammer"  
> beginning developed at Electron.org.uk 2018   
> current maintainer: Dr Andreas Krueger 2018    
> https://github.com/drandreaskrueger/chainhammer    

Consider to submit your improvements & [usage](../docs/other-projects.md) as pull request. Thanks.
