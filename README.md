Public repo because [#346](https://github.com/jpmorganchase/quorum/issues/346), etc - for more info also see Electron-[internal repo](https://gitlab.com/electronDLT/training-material/).
# chainhammer v12
TPS measurements of Quorum, EnergyWebFoundation, etc.

## instructions
* `chainhammer` - submits many transactions to blockchain - see [quorum.md](quorum.md) and [tobalaba.md](tobalaba.md)
* `chainreader` - reads in the whole chain, and visualizes TPS, blocktime, gas, bytes - see [chainreader/README.md](chainreader/README.md)

## faster wider more

See 

* logbook [log.md](log.md) for what I have done to get this faster on Quorum, step by step.
* some ideas what to try next: [TODO.md](TODO.md) = e.g. IBFT, geth/parity PoA, IPC not RPC, Crux not Constellation, etc.


Suggestions please: how can I speed this up further? 

## you
See [other-projects.md](other-projects.md) using this, or which are similar to this. Please report back when you have done other / new measurements. 


## credits


Please credit this as:

> benchmarking scripts "chainhammer"  
> https://gitlab.com/electronDLT/chainhammer    
> by Dr Andreas Krueger, Electron.org.uk, London 2018  

Consider to submit your improvements & [usage](other-projects.md) as pull request. Thanks.
