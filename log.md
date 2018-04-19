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



