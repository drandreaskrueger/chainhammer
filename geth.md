# geth Clique PoA benchmarking
To have a nodes setup comparable to the  quorum [7nodes example](https://github.com/jpmorganchase/quorum-examples/tree/master/examples/7nodes) or the blk.io [crux-quorum-4nodes-docker-compose](https://github.com/blk-io/crux/blob/master/docker/quorum-crux/docker-compose.yaml), I am looking for a ready dockerized or vagrant virtualbox solution. Please tell me if you know a good one. For now I have chosen

## javahippie/geth-dev

```
git clone https://github.com/javahippie/geth-dev javahippie_geth-dev
cd javahippie_geth-dev
```

edit *both* duplicates of the genesis block

```
nano node/genesis.json 
nano miner/genesis.json 
```

and change to these values (faster & larger blocks):

```
    "clique": {
      "period": 2,
    }
  },
...
  "gasLimit": "0x2625A00",
```

(unfortunately, 1 second period, and 20million (0x1312D00) gasLimit (like in my quorum IBFT benchmarks) seems to not work properly here (chain stuck) - so I chose twice the interval and blocksize)

then start with
```
docker-compose up
```

At http://localhost:3000/ you can see an ethstats overview of the three nodes.

### docker stuff

If any changes in those ^ files are not reflected after restarting - try:

    docker-compose build

N.B.: It can take quite some time after restarting, until a new block is created. Before starting a benchmarking, I suggest to always open a JSRE console, and check that the blocknumber is increasing:

    geth attach http://localhost:8545
    eth.blockNumber

To delete the blockchain and start new

    docker-compose down
    docker-compose up

Also see [this issue](https://github.com/javahippie/geth-dev/issues/15).

## results
log of run 1
```
./tps.py 
versions: web3 4.3.0, py-solc: 2.1.0, solc 0.4.23+commit.124ca40d.Linux.gpp, testrpc 1.3.4, python 3.5.3 (default, Jan 19 2017, 14:11:04) [GCC 6.3.0 20170118]
web3 connection established, blockNumber = 13, node version string =  Geth/v1.8.13-stable-225171a4/linux-amd64/go1.10.3
first account of node is 0x3590ACA93338b0721966a8d0C96EbF2C4c87c544, balance is 904625697166532776746648320380374280103671755200316906558.262375061821325312 Ether
nodeName: Geth, nodeType: Geth, consensus: ???, chainName: 500

Block  13  - waiting for something to happen
(filedate 1534775774) last contract address: 0x06FFE7da847332d2B5E8A738db23aEF949b8Fbf2
(filedate 1534777534) new contract address: 0x06FFE7da847332d2B5E8A738db23aEF949b8Fbf2

starting timer, at block 20 which has  1  transactions; at timecode 25953.459564793
block 20 | new #TX   0 / 2000 ms =   0.0 TPS_current | total: #TX    1 /  2.1 s =   0.5 TPS_average
block 21 | new #TX 589 / 2000 ms = 294.5 TPS_current | total: #TX  590 /  4.0 s = 146.2 TPS_average
block 22 | new #TX 805 / 2000 ms = 402.5 TPS_current | total: #TX 1395 /  6.6 s = 213.0 TPS_average
block 23 | new #TX 693 / 2000 ms = 346.5 TPS_current | total: #TX 2088 /  8.1 s = 256.8 TPS_average
block 24 | new #TX 703 / 2000 ms = 351.5 TPS_current | total: #TX 2791 / 10.3 s = 270.4 TPS_average
block 25 | new #TX 696 / 2000 ms = 348.0 TPS_current | total: #TX 3487 / 12.2 s = 285.1 TPS_average
block 26 | new #TX 711 / 2000 ms = 355.5 TPS_current | total: #TX 4198 / 14.4 s = 291.3 TPS_average
block 27 | new #TX 713 / 2000 ms = 356.5 TPS_current | total: #TX 4911 / 16.0 s = 306.8 TPS_average
block 28 | new #TX 699 / 2000 ms = 349.5 TPS_current | total: #TX 5610 / 18.5 s = 302.8 TPS_average
block 29 | new #TX 735 / 2000 ms = 367.5 TPS_current | total: #TX 6345 / 20.2 s = 313.6 TPS_average
block 30 | new #TX 723 / 2000 ms = 361.5 TPS_current | total: #TX 7068 / 22.4 s = 315.3 TPS_average
block 31 | new #TX 669 / 2000 ms = 334.5 TPS_current | total: #TX 7737 / 24.0 s = 322.5 TPS_average
block 32 | new #TX 725 / 2000 ms = 362.5 TPS_current | total: #TX 8462 / 26.5 s = 319.8 TPS_average
block 33 | new #TX 689 / 2000 ms = 344.5 TPS_current | total: #TX 9151 / 28.1 s = 326.0 TPS_average
block 34 | new #TX 721 / 2000 ms = 360.5 TPS_current | total: #TX 9872 / 30.3 s = 325.9 TPS_average
block 35 | new #TX 731 / 2000 ms = 365.5 TPS_current | total: #TX 10603 / 32.2 s = 329.5 TPS_average
block 36 | new #TX 681 / 2000 ms = 340.5 TPS_current | total: #TX 11284 / 34.4 s = 328.3 TPS_average
block 37 | new #TX 695 / 2000 ms = 347.5 TPS_current | total: #TX 11979 / 36.0 s = 332.9 TPS_average
block 38 | new #TX 686 / 2000 ms = 343.0 TPS_current | total: #TX 12665 / 38.5 s = 329.4 TPS_average
block 39 | new #TX 724 / 2000 ms = 362.0 TPS_current | total: #TX 13389 / 40.1 s = 334.1 TPS_average
block 40 | new #TX 729 / 2000 ms = 364.5 TPS_current | total: #TX 14118 / 42.7 s = 330.8 TPS_average
block 41 | new #TX 439 / 2000 ms = 219.5 TPS_current | total: #TX 14557 / 44.1 s = 330.2 TPS_average
block 42 | new #TX 390 / 2000 ms = 195.0 TPS_current | total: #TX 14947 / 46.3 s = 322.8 TPS_average
block 43 | new #TX 448 / 2000 ms = 224.0 TPS_current | total: #TX 15395 / 48.2 s = 319.2 TPS_average
block 44 | new #TX 464 / 2000 ms = 232.0 TPS_current | total: #TX 15859 / 50.2 s = 316.0 TPS_average
block 45 | new #TX 428 / 2000 ms = 214.0 TPS_current | total: #TX 16287 / 52.1 s = 312.7 TPS_average
block 46 | new #TX 467 / 2000 ms = 233.5 TPS_current | total: #TX 16754 / 54.3 s = 308.7 TPS_average
block 47 | new #TX 460 / 2000 ms = 230.0 TPS_current | total: #TX 17214 / 56.1 s = 306.6 TPS_average
block 48 | new #TX 420 / 2000 ms = 210.0 TPS_current | total: #TX 17634 / 58.3 s = 302.3 TPS_average
block 49 | new #TX 432 / 2000 ms = 216.0 TPS_current | total: #TX 18066 / 60.2 s = 299.9 TPS_average
block 50 | new #TX 451 / 2000 ms = 225.5 TPS_current | total: #TX 18517 / 62.5 s = 296.3 TPS_average
block 51 | new #TX 566 / 2000 ms = 283.0 TPS_current | total: #TX 19083 / 64.1 s = 297.7 TPS_average
block 52 | new #TX 569 / 2000 ms = 284.5 TPS_current | total: #TX 19652 / 66.3 s = 296.6 TPS_average
block 53 | new #TX 349 / 2000 ms = 174.5 TPS_current | total: #TX 20001 / 68.1 s = 293.7 TPS_average
block 54 | new #TX   0 / 2000 ms =   0.0 TPS_current | total: #TX 20001 / 70.0 s = 285.8 TPS_average
block 55 | new #TX   0 / 2000 ms =   0.0 TPS_current | total: #TX 20001 / 72.1 s = 277.3 TPS_average
block 56 | new #TX   0 / 2000 ms =   0.0 TPS_current | total: #TX 20001 / 74.0 s = 270.3 TPS_average
block 57 | new #TX   0 / 2000 ms =   0.0 TPS_current | total: #TX 20001 / 76.2 s = 262.6 TPS_average
```
### results approx 350 TPS but only for first 14k transactions 

![https://gitlab.com/electronDLT/chainhammer/raw/master/chainreader/img/geth-clique-2s-gas40mio-RPC_tps-bt-bs-gas_blks21-65.png](https://gitlab.com/electronDLT/chainhammer/raw/master/chainreader/img/geth-clique-2s-gas40mio-RPC_tps-bt-bs-gas_blks21-65.png)
image https://gitlab.com/electronDLT/chainhammer/blob/master/chainreader/img/geth-clique-2s-gas40mio-RPC_tps-bt-bs-gas_blks21-65.png

The following averages are calculated in the zoomed in diagrams at the bottom of notebook [chainreader/blocksDB_analyze_geth-clique.ipynb](https://gitlab.com/electronDLT/chainhammer/blob/master/chainreader/blocksDB_analyze_geth-clique.ipynb)


* we see **approx 350 TPS** when averaging over blocks 23-40 
* then a sudden drop, after ~14,000 transactions (also visible in `TPS_current` in the above table)
* we see **approx 230 TPS** when averaging over blocks 44-53 

The reason for this drop is to be found out, see issue [GE#17447](https://github.com/ethereum/go-ethereum/issues/17447) "Sudden drop in TPS after total 14k transactions".

(actually, [same behavior as in quorum IBFT](https://gitlab.com/electronDLT/chainhammer/blob/master/quorum-IBFT.md#result-400-tps-but-only-for-the-first-14k-tx))

## issues
* [GD#13](https://github.com/javahippie/geth-dev/issues/13) chain is stuck at block 1 or block 2
* [GD#14](https://github.com/javahippie/geth-dev/issues/14) account password?
* [GD#15](https://github.com/javahippie/geth-dev/issues/15) remove chain without rebuilding whole container 
* [GE#17447](https://github.com/ethereum/go-ethereum/issues/17447) Sudden drop in TPS after total 14k transactions
* [GE#17535](https://github.com/ethereum/go-ethereum/issues/17535) how to detect which consensus algorithm is driving the chain?