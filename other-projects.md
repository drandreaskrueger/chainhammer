# other projects & blockchain benchmarks
https://gitlab.com/electronDLT/chainhammer has helped to create these measurements, on different Ethereum type blockchains. Feel free to include it into your project, preferably as a [submodule](https://www.google.co.uk/search?q=git+submodule+how+to), in case this repo keeps on evolving.

To appear in the following lists, please [fork](https://gitlab.com/electronDLT/chainhammer/forks/new) this repo, add your information, and then "pull request". Thanks.

## other blockchain benchmarking projects

* [Cryptocurrency: Scaling Ethereum to 1.5 million TPS](https://steemit.com/blockchain/@andrecronje/cryptocurrency-scaling-ethereum-to-1-5-million-tps)
* IBFT 800 TPS preliminary results - slide 35 in https://www.slideshare.net/YuTeLin1/istanbul-bft 
* CodyBorn Microsoft - signing transactions himself, each transaction comes from a different account --> 400 TPS even with parity, see these answers: [codyborn.md](codyborn.md)
* ...

[please add yours, and pull request]


## theory
* [ESE#58500](https://ethereum.stackexchange.com/questions/58500/how-well-do-proof-of-authority-poa-implementations-of-geth-clique-and-parity) - How well do Proof of Authority (PoA) implementations of Geth (Clique) and Parity (Aura) scale?
  * [eprint](https://eprints.soton.ac.uk/415083/2/itasec18_main.pdf) - PBFT vs Proof-of-Authority: Applying the CAP Theorem to Permissioned Blockchain
  * TODO: read


## projects using chainhammer
* [initial results log.md](log.md); [quorum.md raft](quorum.md) and [quorum-IBFT.md](quorum-IBFT.md), [tobalaba.md](tobalaba.md)
* "**Quorum stress-test 1: 140 TPS**" by vasa (@vaibhavsaini, @vasa-develop, @towardsblockchain) (May 2018)
  * [medium article](https://medium.com/@vaibhavsaini_67863/792f39d0b43f) = instruction, screenshots, results
  * [github repo](https://github.com/vasa-develop/quorum-testnode-1) = compilation from different repos: an updated [7nodes example](https://github.com/jpmorganchase/quorum-examples/pull/93), this chainhammer repo, and an [installation manual](https://gist.github.com/vasa-develop/ff34688c7cb7ae8bb6de9587a4752969#file-dependencies-sh) for Ubuntu AWS
* "Awesome tool, we use it in house" @fixanoid about chainhammer, in [go-quorum.slack.com](https://go-quorum.slack.com/archives/C68NY0QQZ/p1533311592000549?thread_ts=1533286979.000250&cid=C68NY0QQZ)
* "great to hear and thanks for the update! We have also been using chainhammer in our testing." [@jpmsam Aug 18th](https://github.com/jpmorganchase/quorum/issues/346#issuecomment-414086942)
* ...

[please add yours, and pull request]


## this project

### tweets

> Cool, checkout chainhammer, a toolset for benchmarking blockchain TPS by @drandreaskruger / @ElectronDLT
> https://gitlab.com/electronDLT/chainhammer  

https://twitter.com/5chdn/status/1032749019179765760  
https://twitter.com/drandreaskruger/status/1032757116073848834  


### short summary

> Electron created the open source tools `chainhammer` which submits a high load of smart contract transactions to an Ethereum based blockchain, and `chainreader` which reads in the whole chain, and produces diagrams of TPS, blocktime, gasUsed and gasLimit, and the blocksize.
> https://gitlab.com/electronDLT/chainhammer

### credits

    benchmarking scripts "chainhammer"
    https://gitlab.com/electronDLT/chainhammer
    by Dr Andreas Krueger, Electron.org.uk, London
