
# new TODOs while work in progress
* update documentation: 
  * explain new scripts like ./run.sh and ./run-all_....sh
  * radically shorten main README.md = put everything else into docs/chainhammer.md
  * `deploy.py notest` --> `deploy.py`; get-set-get test is now run with `deploy.py andtests`
  * include methodology chapter as manual - perhaps wait until it is read? 
* timestamp transformation = different units depending on client, see tps.timestampToSeconds():
  * next time when trying 'raft' consensus - test whether timestamp transformation is working correctly
  * testrpc-py blocktime is badly estimated - check back with https://github.com/pipermerriam/eth-testrpc/issues/117 if problem is solved now
* parity:
  * parity instantseal produces 1 block per 1 transaction, but with an integer block timestamp - totally non-sensical. Needs finer time resolution!
  * parity v2.x.y breaks down when shot at with multi-threaded sending, so for now chainhammer is testing it only single-threaded. See issue [PE#9582](https://github.com/paritytech/parity-ethereum/issues/9582)
  * parity: why the empty blocks in parity aura runs?
  * parity: accelerate = best combination of CLI parameters when starting parity? That should be IMHO done by parity team because they know their code best; I can just provide the benchmarking platform so that they notice what helps and what not. See [PE#9393](https://github.com/paritytech/parity-ethereum/issues/9393)   
* quorum:
  * even with gasLimit=0x1312D00 (20,000,000), quorum blocks initially max out
  * what is with the higher initial blocktime? Perhaps modify is_up.py to wait for moving chain?
  * run with newer than Geth/v1.7.2-stable-3f1817ea/linux-amd64/go1.10.7, waiting for issue [BC#57](https://github.com/blk-io/crux/issues/57)
  * try also raft consensus, waiting for issue [BC#51](https://github.com/blk-io/crux/issues/51) 
* base tech
  * also try to connect via IPC (currently RPC) - faster?
  * current mempool size, per each node?
* results
  * is it good or bad to store the results (reader/img/ diagrams, results/run/___.html pages) directly in the same repo? Where else?
  * make a new docs/quorum.md, docs/geth.md, etc. per client - and move the issues there!  
  * run everything again, then replace the images on the main README.md
* display
  * multi-terminal tool (e.g terminator), to show all logs/___.log files at once

beware: some of this collection is outdated:

# TODO - next steps

interesting next questions:

* in [Ethereum Core Devs Meeting 49, on Nov 9th 2018](https://github.com/ethereum/pm/issues/60), @Afri mentioned that some people are working on porting `Clique` (the `geth` PoA) to `parity`
  * so soon there can be a cross-client PoA algorithm! Good news. 
  * Will be interesting to combine https://github.com/javahippie/geth-dev and https://github.com/paritytech/parity-deploy !
* [a first issue](https://github.com/drandreaskrueger/chainhammer/issues/1) with python library dependencies for chainhammer was reported 
* add this repo to https://github.com/ConsenSys/ethereum-developer-tools-list
* quorum: solve [this strange problem](https://github.com/drandreaskrueger/chainhammer/blob/d3b408d325e1089c54071aeceb4af06b75133dd2/reproduce_TODO-crux.md#problems) which seems to only appear on Amazon AWS; but no time for this now.
* gas / transaction bytes / block size / ...
  * standard `.set()` call needs `26644 gas`, very small; general calls will be larger --> estimate effect of gas on TPS:
  * custom smart contract that can use *tunable gas* for *storage* (e.g. append to list), or tunable gas for *calculations* (e.g. loop multiplication) instead of the SimpleStorage.sol 
* Vanilla Ethereum PoW
  * to get the baseline TPS using my scripts
* Ethereum PoA tools
  * `geth` perhaps via **--> puppeth** ?
  * [hackernoon](https://hackernoon.com/setup-your-own-private-proof-of-authority-ethereum-network-with-geth-9a0a3750cda8)
  * [stackexchange](https://ethereum.stackexchange.com/questions/15644/setting-up-a-private-poa-clique-network-with-puppeth/15649#15649)
  * [puppeth hints](https://github.com/ethereum/go-ethereum/issues/15581)
* send TX via websockets instead of RPC - faster?
* [doing away with vagrant](log.md#doing-away-with-vagrant), instead run on host machine - tried, BUT have to wait for [severe bug #352](https://github.com/jpmorganchase/quorum/issues/352#issuecomment-384731645) to be fixed; see [non-vagrant/README.md](https://github.com/drandreaskrueger/quorum-examples/blob/e8a368fa5248400472dc1bb66f3de4f38c26d9a9/non-vagrant/README.md)
* [eth_sendTransactionAsync](https://github.com/jpmorganchase/quorum/issues/346#issuecomment-382216968) ??
* [QuorumNetworkManager](https://github.com/ConsenSys/QuorumNetworkManager)
* benchmark EOS / EOSclassic - see [eos.md](../results/eos.md)
* compare all results in a table / barchart, instead of chronological text log files.

what else? Please YOU make suggestions.

N.B.: No guarantees that I will get time to continue with this at all - so please feel invited to fork this repo, and keep on working on benchmarking this. I'll happily merge your pull request. Thanks.

# other places:
* [quorum.md](../results/quorum.md) - quickstart how to use this chainhammer tool
  * [log.md](../results/log.md) - sequence of everything that I've already optimized, to get this faster 
  * [non-vagrant/README.md](https://github.com/drandreaskrueger/quorum-examples/blob/master/non-vagrant/README.md) - attempt to run it on host machine instead of inside vagrant VB; currently broken, issue unanswered.
* [tobalaba.md](../results/tobalaba.md) also benchmarked the parity fork of the EnergyWebFoundation: `--chain Tobalaba`
* [quorum-IBFT.md](../results/quorum-IBFT.md)
* [parity.md](../results/parity.md)
* [reader/](../reader/) chainreader: traverse whole chain, display as 4 diagrams: TPS, size, gas, blocktime
* main [README.md](../README.md) - entry point for this repo, now with quickstart

