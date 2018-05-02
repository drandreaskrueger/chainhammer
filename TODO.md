# TODO - next steps

interesting next questions:

* `IBFT` instead of `raft`
  * generic [7nodes example](https://github.com/drandreaskrueger/quorum-examples/blob/master/examples/7nodes/README.md#7-nodes) contains IBFT already; so that part *should be* easy (however, some issues reported bugs with IBFT ?)
  * needs code update in `tps.py`, see [README.md](README.md) --> IBFT
* [Crux](https://medium.com/blk-io/announcing-crux-a-secure-enclave-for-quorum-61afbfdb79e4) instead of `Constellation`
  * newly developed by blk.io / Conor Svenson
  * already has a "7nodes example", so should be easy to benchmark: [raft](https://github.com/blk-io/quorum-examples/blob/68610ee8ff9aa187d3ba76c92ed2c991c0b59e7b/examples/7nodes/raft-start.sh#L7), [IBFT](https://github.com/blk-io/quorum-examples/blob/68610ee8ff9aa187d3ba76c92ed2c991c0b59e7b/examples/7nodes/istanbul-start.sh#L7)
* Vanilla Ethereum PoW
  * to get the baseline TPS using my scripts
* Vanilla Ethereum PoA
  * perhaps easiest via **--> puppeth** ?
  * [hackernoon](https://hackernoon.com/setup-your-own-private-proof-of-authority-ethereum-network-with-geth-9a0a3750cda8)
  * [stackexchange](https://ethereum.stackexchange.com/questions/15644/setting-up-a-private-poa-clique-network-with-puppeth/15649#15649)
* gas / transaction bytes / block size / ...
  * standard `.set()` call needs `26644 gas`, very small; general calls will be larger --> estimate effect of gas on TPS:
  * custom smart contract that can use *tunable gas* for *storage* (e.g. append to list), or tunable gas for *calculations* (e.g. loop multiplication) instead of the SimpleStorage.sol
* [doing away with vagrant](log.md#doing-away-with-vagrant), instead run on host machine - tried, BUT have to wait for [severe bug #352](https://github.com/jpmorganchase/quorum/issues/352#issuecomment-384731645) to be fixed
* [eth_sendTransactionAsync](https://github.com/jpmorganchase/quorum/issues/346#issuecomment-382216968) ??
* [QuorumNetworkManager](https://github.com/ConsenSys/QuorumNetworkManager)
* compare all results in a table / barchart, instead of chronological text log files.

what else?

N.B.: No guarantees that I will get time to continue with this at all - so please feel invited to fork this repo, and keep on working on benchmarking this. I'll happily merge your pull request. Thanks.

### other places:
* [log.md](log.md) - sequence of everything that I've already optimized, to get this faster
* [README.md](README.md) - quickstart how to use this chainhammer tool
* [Quorum-consensus.md](https://gitlab.com/electronDLT/training-material/blob/master/EEA/Quorum-consensus.md) - raft, IBFT, etc
* [Quorum-privacy.md](https://gitlab.com/electronDLT/training-material/blob/master/EEA/Quorum-privacy.md) - quorum private transactions
* [non-vagrant/README.md](https://github.com/drandreaskrueger/quorum-examples/blob/master/non-vagrant/README.md) - attempt to run it on host machine instead of inside vagrant VB; currently broken, issue unanswered