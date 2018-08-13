# quorum IBFT benchmarking

I have been trying to raise the TPS:

### mempool settings
20,000 transactions cannot be propagated without changing the txpool settings (see [quorum issue 467](https://github.com/jpmorganchase/quorum/issues/467#issuecomment-412536373)):

    --txpool.globalslots 20000 
    --txpool.globalqueue 20000

add to ARGS in [7nodes/istanbul-start.sh](https://github.com/jpmorganchase/quorum-examples/blob/32e7c8d98a6bcf55e4fd74f84192fd9c2cb69487/examples/7nodes/istanbul-start.sh#L20)
```
ARGS="--txpool.globalslots 20000 --txpool.globalqueue 20000 ...
```

### faster blockperiod
the default 7nodes example uses a 5 seconds istanbul.blockperiod, which can be changed with

    --istanbul.blockperiod 1

add to ARGS in [7nodes/istanbul-start.sh](https://github.com/jpmorganchase/quorum-examples/blob/32e7c8d98a6bcf55e4fd74f84192fd9c2cb69487/examples/7nodes/istanbul-start.sh#L20)
```
ARGS="... --istanbul.blockperiod 1 ...
```

### higher gas Limit
in default settings, but high hammering rate ... every block turns out to be full, so I also tried to raise the gaslimit (from the default 4.7 million):

change istanbul-genesis.json to 

--> 20 million gas (["gasLimit": "0x1312D00"](https://github.com/jpmorganchase/quorum-examples/blob/0ccd3eab85e65b73078ecc11ce85dea7459be7ca/examples/7nodes/istanbul-genesis.json#L51))

## example run: 1sec istanbul.blockperiod, 20 million gasLimit

```
./tps.py 

versions: web3 4.3.0, py-solc: 2.1.0, solc 0.4.23+commit.124ca40d.Linux.gpp, testrpc 1.3.4, python 3.5.3 (default, Jan 19 2017, 14:11:04) [GCC 6.3.0 20170118]
web3 connection established, blockNumber = 21, node version string =  Geth/v1.7.2-stable-159d813f/linux-amd64/go1.9.3
first account of node is 0xcA843569e3427144cEad5e4d5999a3D0cCF92B8e, balance is 1000000000 Ether
nodeName: Quorum, nodeType: Geth, consensus: istanbul, chainName: ???

Block  21  - waiting for something to happen
(filedate 1534170380) last contract address: 0x1932c48b2bF8102Ba33B4A6B545C32236e342f34
(filedate 1534171683) new contract address: 0x1932c48b2bF8102Ba33B4A6B545C32236e342f34

starting timer, at block 42 which has  1  transactions; at timecode 131887.871188314
block 42 | new #TX   0 / 1000 ms =   0.0 TPS_current | total: #TX    1 /  1.0 s =   1.0 TPS_average
block 43 | new #TX  88 / 1000 ms =  88.0 TPS_current | total: #TX   89 /  2.6 s =  33.8 TPS_average
block 44 | new #TX 277 / 1000 ms = 277.0 TPS_current | total: #TX  366 /  4.4 s =  83.6 TPS_average
block 45 | new #TX 527 / 1000 ms = 527.0 TPS_current | total: #TX  893 /  7.1 s = 126.6 TPS_average
block 46 | new #TX 600 / 3000 ms = 200.0 TPS_current | total: #TX 1493 / 11.0 s = 135.2 TPS_average
block 47 | new #TX 731 / 3000 ms = 243.7 TPS_current | total: #TX 2224 / 11.7 s = 190.5 TPS_average
block 48 | new #TX 755 / 4000 ms = 188.8 TPS_current | total: #TX 2979 / 18.5 s = 161.3 TPS_average
block 49 | new #TX 756 / 4000 ms = 189.0 TPS_current | total: #TX 3735 / 21.9 s = 170.6 TPS_average
block 50 | new #TX 756 / 4000 ms = 189.0 TPS_current | total: #TX 4491 / 26.4 s = 170.1 TPS_average
block 51 | new #TX 756 / 3000 ms = 252.0 TPS_current | total: #TX 5247 / 30.2 s = 173.8 TPS_average
block 52 | new #TX 756 / 4000 ms = 189.0 TPS_current | total: #TX 6003 / 34.2 s = 175.4 TPS_average
block 53 | new #TX 756 / 4000 ms = 189.0 TPS_current | total: #TX 6759 / 37.6 s = 179.8 TPS_average
block 54 | new #TX 757 / 4000 ms = 189.2 TPS_current | total: #TX 7516 / 38.8 s = 193.5 TPS_average
block 55 | new #TX 757 / 5000 ms = 151.4 TPS_current | total: #TX 8273 / 46.6 s = 177.7 TPS_average
block 56 | new #TX 757 / 4000 ms = 189.2 TPS_current | total: #TX 9030 / 49.3 s = 183.3 TPS_average
block 57 | new #TX 757 / 4000 ms = 189.2 TPS_current | total: #TX 9787 / 55.0 s = 177.8 TPS_average
block 58 | new #TX 757 / 4000 ms = 189.2 TPS_current | total: #TX 10544 / 59.1 s = 178.4 TPS_average
block 59 | new #TX 757 / 4000 ms = 189.2 TPS_current | total: #TX 11301 / 62.7 s = 180.2 TPS_average
block 60 | new #TX 758 / 5000 ms = 151.6 TPS_current | total: #TX 12059 / 67.4 s = 178.9 TPS_average
block 61 | new #TX 758 / 4000 ms = 189.5 TPS_current | total: #TX 12817 / 68.2 s = 187.9 TPS_average
block 62 | new #TX 758 / 4000 ms = 189.5 TPS_current | total: #TX 13575 / 75.8 s = 179.1 TPS_average
block 63 | new #TX 758 / 4000 ms = 189.5 TPS_current | total: #TX 14333 / 80.4 s = 178.3 TPS_average
block 64 | new #TX 758 / 4000 ms = 189.5 TPS_current | total: #TX 15091 / 83.6 s = 180.4 TPS_average
block 65 | new #TX 759 / 4000 ms = 189.8 TPS_current | total: #TX 15850 / 87.9 s = 180.4 TPS_average
block 66 | new #TX 759 / 4000 ms = 189.8 TPS_current | total: #TX 16609 / 91.5 s = 181.5 TPS_average
block 67 | new #TX 759 / 5000 ms = 151.8 TPS_current | total: #TX 17368 / 93.3 s = 186.1 TPS_average
block 68 | new #TX 759 / 1000 ms = 759.0 TPS_current | total: #TX 18127 / 93.7 s = 193.4 TPS_average
block 69 | new #TX 759 / 1000 ms = 759.0 TPS_current | total: #TX 18886 / 95.1 s = 198.6 TPS_average
block 70 | new #TX 760 / 1000 ms = 760.0 TPS_current | total: #TX 19646 / 96.2 s = 204.2 TPS_average
block 71 | new #TX 355 / 1000 ms = 355.0 TPS_current | total: #TX 20001 / 96.7 s = 206.9 TPS_average
block 72 | new #TX   0 / 1000 ms =   0.0 TPS_current | total: #TX 20001 / 97.1 s = 205.9 TPS_average
block 73 | new #TX   0 / 1000 ms =   0.0 TPS_current | total: #TX 20001 / 98.1 s = 203.8 TPS_average
block 74 | new #TX   0 / 1000 ms =   0.0 TPS_current | total: #TX 20001 / 99.2 s = 201.7 TPS_average
block 75 | new #TX   0 / 1000 ms =   0.0 TPS_current | total: #TX 20001 / 99.9 s = 200.2 TPS_average
block 76 | new #TX   0 / 1000 ms =   0.0 TPS_current | total: #TX 20001 / 100.9 s = 198.2 TPS_average
block 77 | new #TX   0 / 1000 ms =   0.0 TPS_current | total: #TX 20001 / 102.0 s = 196.2 TPS_average
block 78 | new #TX   0 / 1000 ms =   0.0 TPS_current | total: #TX 20001 / 103.0 s = 194.2 TPS_average
block 79 | new #TX   0 / 1000 ms =   0.0 TPS_current | total: #TX 20001 / 104.0 s = 192.3 TPS_average
block 80 | new #TX   0 / 1000 ms =   0.0 TPS_current | total: #TX 20001 / 105.0 s = 190.4 TPS_average
block 81 | new #TX   0 / 1000 ms =   0.0 TPS_current | total: #TX 20001 / 106.1 s = 188.6 TPS_average
```

![https://gitlab.com/electronDLT/chainhammer/raw/master/chainreader/img/istanbul-1s-gas20mio_run2_tps-bt-bs-gas_blks40-85.png](https://gitlab.com/electronDLT/chainhammer/raw/master/chainreader/img/istanbul-1s-gas20mio_run2_tps-bt-bs-gas_blks40-85.png)  
https://gitlab.com/electronDLT/chainhammer/blob/master/chainreader/img/istanbul-1s-gas20mio_run2_tps-bt-bs-gas_blks40-85.png

## how to increase the TPS?

any ideas? Please tell us --> 
