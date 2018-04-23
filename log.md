# chainhammer log book of what I tried

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
by varying the [script1.js](script1.js) --> [script3.js](script3.js) 

So I expect constellation to not be in the way.  

Then later the same benchmarking but with `privateFor` field set.  

Then constellation might slow everything down?  


### sending via web3 versus sending via RPC
Samer Falah (@jpmsam) had [suggested](https://github.com/jpmorganchase/quorum/issues/346#issuecomment-382216968) 
that I submit the transactions not via web3, but directly via RPC calls; to speed up the TPS.

So I went through the pain of manually compiling the transaction from ABI, 
method_ID, padded parameter, etc. 
- see [code](https://gitlab.com/electronDLT/chainhammer/blob/9ef7da32443640f2d929b13270a29ac4eef3bc37/send.py#L87-112) 
and then submitting that manually created transaction via requests directly to the JSON-RPC server 
- see [code](https://gitlab.com/electronDLT/chainhammer/blob/9ef7da32443640f2d929b13270a29ac4eef3bc37/send.py#L144-159).

The two choices can be switched with this global constant [ROUTE](https://gitlab.com/electronDLT/chainhammer/blob/9ef7da32443640f2d929b13270a29ac4eef3bc37/send.py#L13).


*Results:*
 
#### blocking (non-async)

100 transactions:

set() via web3: 75.3 TPS_average, 87 TPS peak  
set() via RPC : 75.2 TPS_average, 101 TPS peak  

#### threaded2 (async, queue with 23 workers)
Initially, the nodes crashed quite a few times when trying 1000 transactions, so I started with a smaller number first:

300 transactions:

set() via web3: 153.8 TPS_average, 183 TPS peak  
set() via RPC : 133.0 TPS_average, 235 TPS peak

500 transactions:  

set() via web3: 146.3 TPS_average, 173 TPS peak
set() via RPC : 126.8 TPS_average, 380 TPS peak  

1000 transactions:

set() via web3: 141.9 TPS_average, 209 TPS peak  
set() via RPC : 112.5 TPS_average, 393 TPS peak


So ... calling the JSON-RPC server directly reaches higher peak rates temporarily, 
but then seems to throttle, because the average TPS is considerably lower than  
submitting the transactions with web3.

So - no speed up. Have I lost a whole day of coding now?


### no privateFor (previous chapter), versus `privateFor=["..."]`

TODO, perhaps tomorrow.

