# chainhammer log book of what I tried

## TOC
1. blocking (non-async)
1. async, 1000 threads
1. Two different nodes
1. queue with limited number of multi-threading workers
1. killed the virtualbox, and started anew completely
1. queue with *small* number of multi-threading workers
1. batched multi-threading, no Queue
1. currently the fastest: Queue with 23 workers
1. doing away with vagrant
1. back to vagrant
1. gas
1. non private contract
1. sending via web3 versus sending via RPC; results
1. always resetting the chain before each experiment
1. non-`privateFor` contract
1. contract deployed with `privateFor=["..."]`, but PUBLIC .set()-transactions
1. contract deployed with `privateFor=["..."]`, AND transactions with `privateFor=["..."]`
1. log is continued elsewhere

### blocking (non-async)

13.4 TPS average    
17.1 TPS peak   

### async, 1000 threads

84.2 TPS average  
154 TPS peak  

### 2 different nodes
submit transactions on node 1, but  
query (measure tps) on node 2    

blocking: 13.2 TPS average, 16.6 TPS peak       
async: 92.9 TPS average, 326.1 TPS peak  

### queue with limited number of multi-threading workers

```
./send.py threaded2 42
```
```
  10 workers: 61.8 TPS_average,  78 TPS peak    
  20 workers: 68.3 TPS_average,  97 TPS peak   
  42 workers: 70.5 TPS_average, 116 TPS peak      
  50 workers: 68.8 TPS_average, 128 TPS peak      
 100 workers: 67.8 TPS_average, 206 TPS peak   
 200 workers: 69.4 TPS_average, 180 TPS peak   
 300 workers: 69.7 TPS_average, 193 TPS peak   
 400 workers: 68.5 TPS_average, 196 TPS peak   
 500 workers: 67.2 TPS_average, 305 TPS peak   
 700 workers: 69.1 TPS_average, 175 TPS peak   
1000 workers: 67.9 TPS_average, 202 TPS peak     
```

### killed the virtualbox, and started anew completely
before (chain had grown to 10k blocks)

```
./send.py threaded1
BlockNumber =  10400
send 1000 transactions, multi-threaded, one thread per tx:
```

> 65.6 TPS_average, 127 TPS peak

after redoing [README.md#initialize-7nodes](README.md#initialize-7nodes), the chain is empty again:  


```
BlockNumber =  1
./send.py threaded1
send 1000 transactions, multi-threaded, one thread per tx:

```

> 74.6 TPS_average, 117 TPS peak

It looks as if the TPS go down a bit, when the chain gets longer?


### queue with *small* number of multi-threading workers 

```
./send.py threaded2 10
```
```
   3 workers: 32.0 TPS_average,  38 TPS peak
   5 workers: 44.3 TPS_average,  56 TPS peak
  10 workers: 62.9 TPS_average,  72 TPS peak
  15 workers: 69.5 TPS_average,  85 TPS peak  
  20 workers: 74.7 TPS_average,  82 TPS peak
  25 workers: 74.3 TPS_average,  85 TPS peak                
  30 workers: 72.5 TPS_average,  92 TPS peak       
```

--> multithreading does not need awfully many parallel threads, 25 seems optimal.

### batched multi-threading, no Queue
Even at optimal number of workers (74.3 TPS), 
to use the Queue seemed to have some overhead, 
compared to simple 1000 threads (92.9 TPS) ...
 
So what if we just batch the simple threading.

```
 batch size  25: 62.2 TPS_average,   85 TPS peak 
 batch size  50: 65.6 TPS_average,  140 TPS peak
 batch size 100: 70.2 TPS_average,  122 TPS peak
 batch size 200: 71.3 TPS_average,  112 TPS peak
batch size 1000: 72.2 TPS_average,  108 TPS peak
```

the last is identical to 

```
./send.py threaded1
```
which results in
```
72.4 TPS_average,  135 TPS peak
```

so the initial 92.9 TPS average could not even be replicated anymore; strange.

but in short: thread batching does not help.



### currently the fastest: Queue with 23 workers 

```
./send.py threaded2 23
```
```
23 workers: 73.8 TPS_average,  87 TPS peak       
```

### doing away with vagrant
because [suggested here](https://github.com/jpmorganchase/quorum/issues/346) 

> You can achieve significantly higher TPS:  
> 1. Not running in vagrant  
> ...

Now see repo https://github.com/drandreaskrueger/quorum-examples/tree/master/non-vagrant because pull-request to jpm repo.

**Status quo: quorum crashes**, see [issue #352](https://github.com/jpmorganchase/quorum/issues/352), and [my 'non-vagrant' manual](https://github.com/drandreaskrueger/quorum-examples/blob/master/non-vagrant/README.md)

--> going back to running everything inside vagrant *sigh* .

### back to vagrant

```
rm -rf examples/7nodes/qdata

vagrant up
vagrant ssh

cd quorum-examples/7nodes
./raft-init.sh
./raft-start.sh
sleep 4
./runscript.sh script3.js # script3.js deploys contract WITHOUT privateFor parameter
```

### gas

Turns out the above transactions had all failed 
(even though they made it into the chain, and 
drove raft into making new blocks), 
because `gas=90000` has to be set manually as an input parameter.  
 
A typical `set(7)` transaction needs `gas=26644`.


### non private contract
First I will now benchmark **quorum raft** without setting the `privateFor` field,
by varying the `script1.js` --> `script3.js` 

So I expect constellation to not be in the way.  

Then later the same benchmarking but with `privateFor` field set.  

Then constellation might slow everything down?  


### sending via web3 versus sending via RPC
Samer Falah (@jpmsam) had [suggested](https://github.com/jpmorganchase/quorum/issues/346#issuecomment-382216968) 
that I submit the transactions not via web3, but directly via RPC calls; to speed up the TPS.

So I went through the pain of manually compiling the transaction from ABI, 
method_ID, padded parameter, etc. - see 
[code](https://github.com/drandreaskrueger/chainhammer/blob/9ef7da32443640f2d929b13270a29ac4eef3bc37/send.py#L87-112) 
and then submitting that manually created transaction via requests directly to the JSON-RPC server - see 
[code](https://github.com/drandreaskrueger/chainhammer/blob/9ef7da32443640f2d929b13270a29ac4eef3bc37/send.py#L144-159).

The two choices can be switched with this global constant [ROUTE](https://github.com/drandreaskrueger/chainhammer/blob/9ef7da32443640f2d929b13270a29ac4eef3bc37/send.py#L13).


*Results:*
 
#### blocking (non-async)

100 transactions:

```
set() via web3: 75.3 TPS_average, 87 TPS peak  
set() via RPC : 75.2 TPS_average, 101 TPS peak  
```

#### threaded2 (async, queue with 23 workers)
Initially, the nodes crashed quite a few times when trying 1000 transactions, so I started with a smaller number first:

300 transactions:
```
set() via web3: 153.8 TPS_average, 183 TPS peak  
set() via RPC : 133.0 TPS_average, 235 TPS peak
```

500 transactions:  
```
set() via web3: 146.3 TPS_average, 173 TPS peak
set() via RPC : 126.8 TPS_average, 380 TPS peak  
```
1000 transactions:
```
set() via web3: 141.9 TPS_average, 209 TPS peak  
set() via RPC : 112.5 TPS_average, 393 TPS peak
```

So ... calling the JSON-RPC server directly reaches higher peak rates temporarily, 
but then seems to throttle, because the average TPS is considerably lower than  
submitting the transactions with web3.

So - **no speed increase**. 

*Have I lost a whole day of coding now?*


### always resetting the chain before each experiment:
Longer chain / previously hammered system ... seems to lower the TPS - really?  
Sadly, that seems to be the case; so for better accuracy, I always reset before each experiment.  

Quick-reset:
```
./stop.sh; ./raft-init.sh; ./raft-start.sh; sleep 4; ./runscript.sh script3.js 
```

#### non-`privateFor` contract
contract deployed with `script3.js` 

blocking (non-async):
```
web3: 93.4 TPS_average, 105 TPS peak  
RPC : 98.5 TPS_average, 114 TPS peak  
```

async, 1000 threads; `send.py threaded1`
```
web3: 129.3 TPS_average, 203 TPS peak
RPC : 146.3 TPS_average, 307 TPS peak
```

async, queue 23, workers; `send.py threaded2 23`
```
web3: 149.2 TPS_average, 183 TPS peak
RPC : 177.1 TPS_average, 270 TPS peak 
```

**Summary: (As constellation is not needed,) public contracts are fastest.** 

#### contract deployed with `privateFor=["..."]`, but PUBLIC .set()-transactions 

contract deployed with `script1.js`

and for each experiment start again at block 1:
```
./stop.sh; ./raft-init.sh; ./raft-start.sh; sleep 4; ./runscript.sh script1.js
```
always 1000 transactions.  

blocking (non-async):
```
web3: 85.2 TPS_average, 109 TPS peak  
RPC : 91.4 TPS_average, 160 TPS peak  
```

async, 1000 threads; `send.py threaded1`
```
web3: 132.2 TPS_average, 267 TPS peak
RPC : 111.4 TPS_average, 350 TPS peak
```

async, queue, 23 workers; `send.py threaded2 23`
```
web3: 143.0 TPS_average, 243 TPS peak
RPC : 136.8 TPS_average, 248 TPS peak 
```

**Summary: Private contracts slow down also public transactions, but only a bit.**

#### contract deployed with `privateFor=["..."]`, AND transactions with `privateFor=["..."]` 

contract deployed with `script1.js`; and for each experiment re-start again at block 1:
```
./stop.sh; ./raft-init.sh; ./raft-start.sh; sleep 4; ./runscript.sh script1.js
```
always 1000 transactions.  

blocking (non-async):
```
web3: 61.6 TPS_average, 78 TPS peak  
RPC : 62.8 TPS_average, 83 TPS peak  
```

async, 1000 threads; `send.py threaded1`
```
web3:  82.7 TPS_average, 134 TPS peak
RPC :  78.8 TPS_average, 133 TPS peak
```

async, queue, 23 workers; `send.py threaded2 23`
```
web3:  89.6 TPS_average, 138 TPS peak
RPC :  83.9 TPS_average, 129 TPS peak 
```

**Summary: Private transactions cause 30% - 50% lower TPS than public transactions.**


### pause now

I must pause this for now.  Last steps for wrapping it up:
* added more infos to the [open issue #352](https://github.com/jpmorganchase/quorum/issues/352)
* new [TODO.md](../docs/TODO.md) with possible next steps - feel free to fork this, and work on it. Thanks.

## log is continued elsewhere
see

* [quorum.md](quorum.md)
* [quorum-IBFT.md](quorum-IBFT.md)
* [tobalaba.md](tobalaba.md)

