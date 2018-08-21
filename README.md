Public repo because [#346](https://github.com/jpmorganchase/quorum/issues/346), etc - for more info also see Electron-[internal repo](https://gitlab.com/electronDLT/training-material/).
# chainhammer v22
TPS measurements of Quorum, EnergyWebFoundation, etc. - should work with any Ethereum type chain

## instructions
* `chainhammer` - submits many transactions to blockchain - see [quorum.md](quorum.md), [quorum-IBFT.md](quorum-IBFT.md), [tobalaba.md](tobalaba.md), and [parity.md](parity.md)
* `chainreader` - reads in the whole chain, and visualizes TPS, blocktime, gas, bytes - see [chainreader/README.md](chainreader/README.md)

## faster wider more

See 

* logbook [log.md](log.md) for what I had done initially to get this faster *on Quorum*, step by step. 
* some ideas what to try next: [TODO.md](TODO.md) = e.g. IBFT, geth/parity PoA, IPC not RPC, Crux not Constellation, etc.


Suggestions please: how can I speed this up further? 

## you
See [other-projects.md](other-projects.md) using this, or projects which are similar to this. 

Please report back when you have done other / new measurements. 

## dependencies
```
pip install virtualenv
virtualenv -p python3 py3eth
source py3eth/bin/activate
python3 -m pip install --upgrade pip==9.0.3
pip3 install --upgrade py-solc==2.1.0 web3==4.3.0 web3[tester]==4.3.0 rlp==0.6.0 eth-testrpc==1.3.4 requests 
```
all python scripts & jupyer notebooks must be run within that virtualenv:

```
source py3eth/bin/activate
./tps.py 
```
etc

## credits

Please credit this as:

> benchmarking scripts "chainhammer"  
> https://gitlab.com/electronDLT/chainhammer    
> by Dr Andreas Krueger, Electron.org.uk, London 2018  

Consider to submit your improvements & [usage](other-projects.md) as pull request. Thanks.

### short summary

> Electron created the open source tools chainhammer which submits a high load of smart contract transactions to an Ethereum based blockchain, and chainreader which reads in the whole chain, and produces diagrams of TPS, blocktime, gasUsed and gasLimit, and the blocksize.
> https://gitlab.com/electronDLT/chainhammer

---

---

---

## chainhammer --> chainreader -->  diagrammer

### quorum raft
[quorum.md](quorum.md) = Quorum (geth fork), raft consensus, 1000 transactions multi-threaded with 23 workers, average TPS around 160 TPS, and 20 raft blocks per second)
![chainreader/img/quorum_tps-bt-bs-gas_blks242-357.png](chainreader/img/quorum_tps-bt-bs-gas_blks242-357.png)

### quorum IBFT
[quorum-IBFT.md](quorum-IBFT.md) = Quorum (geth fork), IBFT consensus, 20 millions gasLimit, 1 second istanbul.blockperiod; 20000 transactions multi-threaded with 13 workers. Initial average >450 TPS then drops to ~270 TPS, see [quorum issue](https://github.com/jpmorganchase/quorum/issues/479#issuecomment-413603316))

![https://gitlab.com/electronDLT/chainhammer/raw/master/chainreader/img/istanbul-crux-docker-1s-gas20mio-RPC_run8_tps-bt-bs-gas_blks28-93.png](https://gitlab.com/electronDLT/chainhammer/raw/master/chainreader/img/istanbul-crux-docker-1s-gas20mio-RPC_run8_tps-bt-bs-gas_blks28-93.png)

### tobalaba
[tobalaba.md](tobalaba.md) = Public "Tobalaba" chain of the EnergyWebFoundation (parity fork), PoA; 20k transactions; > 150 TPS if client is well-connected.

![chainreader/img/tobalaba_tps-bt-bs-gas_blks5173630-5173671.png](chainreader/img/tobalaba_tps-bt-bs-gas_blks5173630-5173671.png)

### parity aura v1.11.8
[parity.md](parity.md) = Initial unoptimized parity run; using `parity-poa-playground` dockerized network of 6 local nodes (3 authorities, 3 members) with 6 billion gasLimit, and mostly 3 seconds blocktime; 20k transactions; > 60 TPS. 

![chainreader/img/parity-poa-playground_run1_tps-bt-bs-gas_blks108-211.png](chainreader/img/parity-poa-playground_run1_tps-bt-bs-gas_blks108-211.png)

Calling all parity experts: How to improve this?
