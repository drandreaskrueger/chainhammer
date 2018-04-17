# chainhammer v04
Quorum raft TPS measurements. Uses the [quorum-examples --> 7nodes](https://github.com/jpmorganchase/quorum-examples/blob/master/examples/7nodes/README.md) example.

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
./runscript.sh script1.js
```
if that says sth like

> Contract transaction send: TransactionHash: 0x00594... waiting to be mined...  
> true

then we now have a block 1 transaction 0 which contains a simple set()/get() smart contract, which we will later fire our transactions at.

see [send.py](send.py) --> ` initialize(contractTx_blockNumber=1, contractTx_transactionIndex=0)`


## start listener

```
python tps.py
```

## start hammering

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
 
max rate that I have seen was 91 TPS.

### multithreaded 2

with an optimized number of parallel threads, i.e. a couple of hundred threads?

TODO: find that sweet spot, if it exists.

## example output

```
Block  711  - waiting for something to happen

starting timer, at block 712 which has  1  transactions; at timecode 1523983206.39
block 712 | #TX 6 / 0.09 seconds = 64.69 TPS
block 714 | #TX 34 / 0.89 seconds = 38.00 TPS
block 723 | #TX 81 / 1.80 seconds = 45.01 TPS
block 731 | #TX 103 / 2.66 seconds = 38.77 TPS
block 737 | #TX 171 / 3.77 seconds = 45.39 TPS
block 747 | #TX 214 / 4.30 seconds = 49.74 TPS
block 752 | #TX 261 / 5.06 seconds = 51.62 TPS
block 756 | #TX 325 / 6.39 seconds = 50.89 TPS
block 768 | #TX 365 / 7.60 seconds = 48.04 TPS
block 781 | #TX 413 / 8.63 seconds = 47.85 TPS
block 787 | #TX 482 / 9.22 seconds = 52.26 TPS
block 797 | #TX 516 / 9.83 seconds = 52.50 TPS
block 807 | #TX 631 / 10.38 seconds = 60.81 TPS
block 822 | #TX 1000 / 10.98 seconds = 91.08 TPS
```

## suggestions please
how can I speed this up?


