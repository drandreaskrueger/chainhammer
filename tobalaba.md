**this is not ready yet**

**scripts might have flaws still**

**do not use yet**


# other clients
Purpose: Extending this to benchmark other Ethereum-type chains.


### start node
    
parity Toabalaba energywebfoundation

     ./target/release/parity --geth --chain tobalaba --rpcapi "web3,eth,personal"
     

parity main chain (untested):

    parity --geth --rpcapi "web3,eth,personal"

    
### account, password

By default, the [deploy.py](deploy.py) uses the first address `web3.eth.accounts[0]`.    
Put your `unlockAccount` passphrase into the file `account-passphrase.txt` (the passphrase must not have whitespaces at the beginning or end).  

### make sure not overflooded already

see e.g.

Tobalaba: https://tobalaba.etherscan.com/txsPending

If there are many, then wait a while.

### start listener
set `RAFT=False` and:

    ./tps.py


### deploy, start sending

    ./deploy.py notest; ./send.py 

or

    ./deploy.py notest; ./send.py threaded2 23

after each experiment, restart the listener, and redeploy the contract.


## results

### Tobalaba

in [config.py](config.py) manually set:
```
RPCaddress, RPCaddress2 = 'http://localhost:8545', 'http://localhost:8545'
RAFT=False
```
then

    ./tps.py

then 

    ./deploy.py notest; ./send.py threaded2 23


preliminary results, might not be 100% true, need more time for debugging, cross-checking, etc


```
./deploy.py notest; ./send.py 

versions: web3 4.2.0, py-solc: 2.1.0, solc 0.4.23+commit.124ca40d.Linux.gpp, testrpc 1.3.4, python 3.5.3 (default, Jan 19 2017, 14:11:04) [GCC 6.3.0 20170118]
web3 connection established, blockNumber = 4305868, node version string =  Energy Web//v1.11.0-unstable-39a38d3fd-20180425/x86_64-linux-gnu/rustc1.25.0
first account of node is 0x0056D95f4c3F1f0B32B538E3BdD393D8e4850857, balance is 59.999704526921853849 Ether
unlock:  True
tx_hash =  0x2c5d7a1ad9f8f17e8278b7483dcf89665db200287daa0c1553709462445b6e76 --> waiting for receipt ...
Deployed. gasUsed=127173 contractAddress=0x8Ce5D80FC631C2f829e3890EF8943Ea8a1dC8102
BlockNumber =  4305869
send 1000 transactions, non-async, one after the other:
[sent via web3] set() transaction submitted:  0x59399ac22a2eadcb2420341db0495c1b823082d6827f578efffc7adeecf69152
...
[sent via web3] set() transaction submitted:  0xc057975a58182d43a2eecb08d6a0b21745b1254a6550dce81790d0bc2b28b831
```

results:

```
./tps.py

versions: web3 4.2.0, py-solc: 2.1.0, solc 0.4.23+commit.124ca40d.Linux.gpp, testrpc 1.3.4, python 3.5.3 (default, Jan 19 2017, 14:11:04) [GCC 6.3.0 20170118]

Block  4305867  - waiting for something to happen

starting timer, at block 4305869 which has  1  transactions; at timecode 34480.607266957
block 4305869 | new #TX  30 / 3000 ms =  10.0 TPS_current | total: #TX   31 /  3.0 s =  10.2 TPS_average
block 4305870 | new #TX  81 / 2000 ms =  40.5 TPS_current | total: #TX  112 /  6.1 s =  18.5 TPS_average
block 4305871 | new #TX  82 / 7000 ms =  11.7 TPS_current | total: #TX  194 / 12.1 s =  16.0 TPS_average
block 4305872 | new #TX 100 / 12000 ms =   8.3 TPS_current | total: #TX  294 / 24.3 s =  12.1 TPS_average
block 4305873 | new #TX  81 / 18000 ms =   4.5 TPS_current | total: #TX  375 / 42.1 s =   8.9 TPS_average
block 4305874 | new #TX  13 / 3000 ms =   4.3 TPS_current | total: #TX  388 / 45.2 s =   8.6 TPS_average
block 4305875 | new #TX  72 / 3000 ms =  24.0 TPS_current | total: #TX  460 / 48.3 s =   9.5 TPS_average
block 4305876 | new #TX   0 / 6000 ms =   0.0 TPS_current | total: #TX  460 / 54.1 s =   8.5 TPS_average
block 4305877 | new #TX  85 / 12000 ms =   7.1 TPS_current | total: #TX  545 / 66.1 s =   8.2 TPS_average
block 4305878 | new #TX   0 / 18000 ms =   0.0 TPS_current | total: #TX  545 / 83.9 s =   6.5 TPS_average
block 4305879 | new #TX   3 / 3000 ms =   1.0 TPS_current | total: #TX  548 / 87.3 s =   6.3 TPS_average
block 4305880 | new #TX  81 / 3000 ms =  27.0 TPS_current | total: #TX  629 / 90.0 s =   7.0 TPS_average
block 4305881 | new #TX  82 / 6000 ms =  13.7 TPS_current | total: #TX  711 / 96.2 s =   7.4 TPS_average
block 4305882 | new #TX   3 / 12000 ms =   0.2 TPS_current | total: #TX  714 / 107.9 s =   6.6 TPS_average
block 4305883 | new #TX  81 / 18000 ms =   4.5 TPS_current | total: #TX  795 / 126.0 s =   6.3 TPS_average
block 4305884 | new #TX   4 / 3000 ms =   1.3 TPS_current | total: #TX  799 / 129.1 s =   6.2 TPS_average
block 4305885 | new #TX  80 / 3000 ms =  26.7 TPS_current | total: #TX  879 / 132.1 s =   6.7 TPS_average
block 4305886 | new #TX   2 / 6000 ms =   0.3 TPS_current | total: #TX  881 / 138.0 s =   6.4 TPS_average
block 4305887 | new #TX  83 / 12000 ms =   6.9 TPS_current | total: #TX  964 / 150.3 s =   6.4 TPS_average
block 4305888 | new #TX  81 / 18000 ms =   4.5 TPS_current | total: #TX 1045 / 168.1 s =   6.2 TPS_average
block 4305889 | new #TX   5 / 3000 ms =   1.7 TPS_current | total: #TX 1050 / 171.2 s =   6.1 TPS_average
block 4305890 | new #TX   0 / 3000 ms =   0.0 TPS_current | total: #TX 1050 / 173.9 s =   6.0 TPS_average
block 4305891 | new #TX   0 / 6000 ms =   0.0 TPS_current | total: #TX 1050 / 180.1 s =   5.8 TPS_average
```

**1000 transactions --> 6-7 TPS on average --> as fast (or slow) as Ethereum PoW ?**


# important disclaimer
**this is not ready yet**

**scripts might have flaws still**

**do not use yet**

