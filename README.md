# chainhammer 
v04

## initialize quorum-examples 7nodes system

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
./runscript.sh script1.js
```
if that says sth like

> Contract transaction send: TransactionHash: 0x00594... waiting to be mined...  
> true

then we now have a block 1 transaction 0 which contains a simple set()/get() smart contract, which we will later fire our transactions at.

see `send.py` --> ` initialize(contractTx_blockNumber=1, contractTx_transactionIndex=0)`


## start listener

```
python tps.py
```

## start hammerer

### blocking
```
python send.py
```

I could see about 12-15 tps max.

### multithreaded 1

you must kill (`CTRL-C`), and restart the listener, then:

```
python send.py threaded1
```
 
max rate that I have seen was 91.07 TPS.

### multithreaded 2

with an optimized maximum number of parallel threads.

TODO.