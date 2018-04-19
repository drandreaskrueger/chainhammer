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

after (chain empty again):

```
vagrant destroy
vagrant up
vagrant ssh
cd quorum-examples/7nodes
./raft-init.sh
./raft-start.sh
sleep 3
./runscript.sh script1.js
exit
```

> 74.6 TPS_average, 117 TPS peak

