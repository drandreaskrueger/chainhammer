N.B.: Work in progress

# chainhammer reproduce results
Tested on and optimized for a Debian AWS machine (based on `debian-stretch-hvm-x86_64-gp2-2018-11-10-63975`) - see [cloud.md](cloud.md) for details.

## TOC

* How to replicate the results
  * install toolchain
  * all 5 experiments in one go
  * run one experiment separately
* AWS --> measurement results 
  * [numbers](#results) <-- jump here if you have only 1 minute -->
  * configurations used
* issues raised while doing this


## How to replicate the results
In recent chainhammer versions, *automation* has done a quantum leap; the whole thing can now be run in TWO LINES, and a bit of patience, waiting for the results coming in:

### toolchain

Now all preparations are done via one script. Please do yourself the favor, and read the source code BEFORE you execute:

    scripts/install.sh

Because this script makes lasting changes to the machine it is running on, so I suggest that you DO NOT USE YOUR MAIN MACHINE! Instead **use a disposable cloud droplet, or virtualbox machine.**

### all 5 experiments in one go

Given a distinguishing prefix for the machine in `$CH_MACHINE`, the 2 scripts

    CH_MACHINE=$HOSTNAME run-all_{small,large}.sh

send about {20,200} seconds worth of transactions at each of the 5 clients (testrpc-py, geth clique, quorum-crux with IBFT, parity-instantseal, parity-aura), while producing diagrams and human readable MD/HTML pages for each of them. 

**A whole laboratory in a one liner!**

Now scroll down to the results! ONLY if you want to know more, continue reading here:

### one experiment

The new `./run.sh` is massively automated now, executing a sequence of 10 steps to run and even already *analyze* a whole experiment. 

    ./run.sh IDENTIFIER [networkstarter-stub]

If a 2nd CLI argument $2 is given, `./run.sh` uses the scripts networks/$2-start.sh and networks/$2-stop.sh for the Ethereum network (or it expects one to be running already on port :8545, if no 2nd argument is given).

It needs 2 ENV variables to be set, `$CH_TXS` for number-of-transactions, and `$CH_THREADING` for the send-algorithm `sequential` or `threaded2` - and for the latter the number of multi-threading workers (thus the quotation marks).

The 1st CLI argument is a human readable title to later distinguish the diagrams, here I choose the `$HOSTNAME` of your machine, but you can choose (an alphanumeric name) freely:

#### example run.sh calls 

e.g. `geth` configuration is hardcoded already in my fork of 'geth-dev', so it is just:

    CH_TXS=30000 CH_THREADING="threaded2 20" ./run.sh $HOSTNAME-Geth geth-clique

while `quorum` and `parity` need to be configured first:

e.g.

    networks/quorum-configure.sh
    CH_TXS=50000 CH_THREADING="threaded2 20" ./run.sh $HOSTNAME-Quorum quorum

or

    networks/parity-configure-aura.sh v2.2.3
    CH_TXS=20000 CH_THREADING="sequential" ./run.sh $HOSTNAME-Parity parity

For now, parity v2.x.y can only handle `sequential` sending. Please you help the parity team to figure out a parity configuration which does not die when shot at with 20 multi-threading workers, see [PE#9582](https://github.com/paritytech/parity-ethereum/issues/9582).




## results

Outdated table in which I had run each of the experiments *manually* in autumn 2018; *soon* re-done completely, using the above automation. So please contact me *now*, if you know how to accelerate any of these clients:

| hardware  	| node type 	    | #nodes 	| config 	| peak TPS_av 	| final TPS_av 	|
|-----------	|-----------	    |--------	|--------	|-------------	|--------------	|
| t2.micro 	    | parity aura   	| 4      	| (D)    	| 45.5        	|  44.3        |
| t2.large 	    | parity aura   	| 4      	| (D)    	| 53.5        	|  52.9        |
| t2.xlarge 	| parity aura   	| 4      	| (J)    	| 57.1        	|  56.4        |
| t2.2xlarge 	| parity aura   	| 4      	| (D)    	| 57.6        	|  57.6        |
|               |                   |           |        	|         	    |              |
| t2.micro 	    | parity instantseal | 1      	| (G)    	| 42.3        	|  42.3        |
| t2.xlarge	    | parity instantseal | 1      	| (J)    	| 48.1        	|  48.1        |
|               |                   |           |        	|         	    |              |
| t2.2xlarge 	| geth clique     	| 3+1 +2    | (B)    	| 421.6       	| 400.0        |
| t2.xlarge 	| geth clique     	| 3+1 +2    | (B)    	| 386.1       	| 321.5        |
| t2.xlarge 	| geth clique     	| 3+1       | (K)    	| 372.6       	| 325.3        |
| t2.large 	    | geth clique     	| 3+1 +2    | (B)    	| 170.7       	| 169.4        |
| t2.small 	    | geth clique     	| 3+1 +2    | (B)    	|  96.8       	|  96.5        |
| t2.micro 	    | geth clique     	| 3+1       | (H)    	| 124.3       	| 122.4        |
|               |                   |           |        	|         	    |              |
| t2.micro SWAP | quorum crux IBFT 	| 4    	    | (I) SWAP! |  98.1         |  98.1   	   |
|               |                   |           |        	|         	    |              |
| t2.micro 	    | quorum crux IBFT 	| 4    	    | (F)     	| lack of RAM   |         	   |
| t2.large 	    | quorum crux IBFT 	| 4    	    | (F)    	| 207.7      	| 199.9        |
| t2.xlarge 	| quorum crux IBFT 	| 4    	    | (F)    	| 439.5      	| 395.7        |
| t2.xlarge 	| quorum crux IBFT 	| 4    	    | (L)    	| 389.1      	| 338.9        |
| t2.2xlarge 	| quorum crux IBFT 	| 4    	    | (F)    	| 435.4      	| 423.1        |
| c5.4xlarge 	| quorum crux IBFT 	| 4    	    | (F)    	| 536.4      	| 524.3        |

For the hardware types, number of CPUs etc - see https://aws.amazon.com/ec2/instance-types/t2/#Product_Details

Only `t2.micro` is *"free tier"*, i.e. please contact me, if you can support me financially, so I can keep testing this on larger machines.

We need completely new ideas how to accelerate parity.

### (A) parity aura  
4 nodes via [paritytech/parity-deploy](https://github.com/paritytech/parity-deploy) with higher gasLimit and gasFloorTarget, and some CLI parameters changed (*you knowledgable parity experts, please experiment with those, to increase the TPS - thanks*):
```
cd ~/paritytech_parity-deploy
# sed -i 's/0x1312D00/0x2625A00/g' config/spec/genesis/aura; cat config/spec/genesis/aura # hardcoded now in parity-deploy https://github.com/paritytech/parity-deploy/issues/55#issuecomment-422309365

./parity-deploy.sh --nodes 4 --config aura --name myaura --geth --jsonrpc-server-threads 10 --tx-queue-size 20000 --cache-size 4096 --gas-floor-target 40000000 --tx-queue-mem-limit 0
cp ~/paritytech_parity-deploy/deployment/1/password ~/drandreaskrueger_chainhammer/account-passphrase.txt
docker-compose up
```
> Parity/v1.11.11-stable-cb03f38-20180910/x86_64-linux-gnu/rustc1.28.0

### (B) geth clique
1 bootnode, and 3 miners nodes, and ethstats client and server, all dockerized. 

Two parameters changed: [gasLimit=40m and clique.period=2 seconds](https://github.com/drandreaskrueger/geth-dev/commit/e1fe5ab4c464e406e3898cbe0152d3c1aa4c6697).
```
cd ~/drandreaskrueger_geth-dev/
docker-compose up
```
> Geth/v1.8.14-stable-316fc7ec/linux-amd64/go1.10.3

### (C) geth quorum IBFT
TODO, some unsolved issues. What worked fine on my local machine does not seem to work anymore on AWS. Strange.

### (D) parity v1.11.11 because 2.0.5 is broken

Unfortunately, they have named `2.0.5` now into `stable` prematurely, so that `docker run parity/parity:stable` starts `parity:v2.0.x` and not `parity:v1.11.x` anymore. 

That *broke everything*, see [parity.md --> run 11](../results/parity.md). 

To correct that, replace `:stable` with the old version `:v1.11.11` *after* running `parity-deploy.sh` (I had also made a [feature request issue](https://github.com/paritytech/parity-deploy/issues/55) about this):
```
cd paritytech_parity-deploy
sudo ./clean.sh
docker kill $(docker ps -q); docker rm $(docker ps -a -q); docker rmi $(docker images -q)

ARGS="--db-compaction ssd --tracing off --gasprice 0 --gas-floor-target 100000000000 "
ARGS=$ARGS"--pruning fast --tx-queue-size 32768 --tx-queue-mem-limit 0 --no-warp "
ARGS=$ARGS"--jsonrpc-threads 8 --no-hardware-wallets --no-dapps --no-secretstore-http "
ARGS=$ARGS"--cache-size 4096 --scale-verifiers --num-verifiers 16 "

./parity-deploy.sh --nodes 4 --config aura --name myaura --geth $ARGS

sed -i 's/parity:stable/parity:v1.11.11/g' docker-compose.yml

docker-compose up
```

### (E) include all current recommendations of parity team:

Use (D) plus `--force-sealing` plus change the blocktime `stepDuration` to 5 seconds, because [5chdn said so](https://github.com/paritytech/parity-ethereum/issues/9586#issuecomment-422717091):

```
cd ~/paritytech_parity-deploy
sudo ./clean.sh

docker kill $(docker ps -q); docker rm $(docker ps -a -q); docker rmi $(docker images -q)

ARGS="--db-compaction ssd --tracing off --gasprice 0 --gas-floor-target 100000000000 "
ARGS=$ARGS"--pruning fast --tx-queue-size 32768 --tx-queue-mem-limit 0 --no-warp "
ARGS=$ARGS"--jsonrpc-threads 8 --no-hardware-wallets --no-dapps --no-secretstore-http "
ARGS=$ARGS"--cache-size 4096 --scale-verifiers --num-verifiers 16 --force-sealing "

./parity-deploy.sh --nodes 4 --config aura --name myaura --geth $ARGS

sed -i 's/parity:stable/parity:v1.11.11/g' docker-compose.yml
jq ".engine.authorityRound.params.stepDuration = 5" deployment/chain/spec.json > tmp; mv tmp deployment/chain/spec.json

docker-compose up
```
This ^ (E) is the newest set of suggested settings, but they actually do not accelerate over the results of the already measured settings (D).

### (F) quorum IBFT settings

Standard dockerized quorum-crux but with a local build, so that these parameters can be tuned before the docker containers are built:

```
gasLimit = "0x1312D00"

--txpool.globalslots 20000 
--txpool.globalqueue 20000 
--istanbul.blockperiod 1
```

See above [#quorum-crux-ibft](#quorum-crux-ibft) for how to do that.

Tried the same with increasing machine sizes, up to 16 vCPUs. Best result 524-536 TPS.

### (G) parity instantseal
```
cd ~/paritytech_parity-deploy
sudo ./clean.sh
docker kill $(docker ps -q); docker rm $(docker ps -a -q); docker rmi $(docker images -q)

./parity-deploy.sh --config dev --name instantseal --geth 

sed -i 's/parity:stable/parity:v1.11.11/g' docker-compose.yml

docker-compose up
```

#### interesting observation:
The blocking version of `send.py` is actually a bit *faster* than the multi-threaded, i.e. hammering with `./deploy.py notest; ./send.py` (instead of `./deploy.py notest; ./send.py threaded2 23`) results in the fastest TPS. 

Is parity essentially single-threaded? 

Also, the go client `geth` benefits greatly from larger machines, i.e. more CPUs; but `parity` shows only very mildly faster TPS on larger machines.

### (H) geth on t2.micro
to make it work on the AWS "free tier" machine, I removed the ethstats docker "geth-monitor-front/backend" - see issue [GD#33](https://github.com/javahippie/geth-dev/issues/33):

```
cd ~/drandreaskrueger_geth-dev
nano docker-compose-without-ethstats.yml
docker-compose -f docker-compose-without-ethstats.yml up --build
```

and even on that small machine I could see well over 100 TPS with geth clique!

### (I) quorum-crux on t2.micro with swapping
To run this 4 nodes dockerized blk-io/crux setup is more difficult because each node runs an instance of geth_quorum AND an instance of crux. I have already posted a [feature request BC#48](https://github.com/blk-io/crux/issues/48) = it would be nice to still be able to run this on a t2.micro all in RAM. For now, you can enlarge the swapfile:
```
sudo swapoff -a && SWAPFILE=/swapfile; sudo dd if=/dev/zero of=$SWAPFILE bs=1M count=1500 && sudo chmod 600 $SWAPFILE && sudo mkswap $SWAPFILE && sudo swapon -a && free -m
```
and keep an instance of `htop` open to notice when the ceiling is hit (the you get connection problems because node 1 or 2 has run out of memory, and crashed):
```
ssh chainhammer
htop
```

other than that, this is identical to (F) above:

```
cd ~/blk-io_crux/docker/quorum-crux
docker-compose -f docker-compose-local.yaml up --build
```

**beware that these results are artifically slow** because swapping not RAM. But I could get it running on an AWS `t2.micro` which is "free tier" - so you can reproduce it without paying!!!

### (J) parity v1.11.11 on AWS t2.xlarge
Repeated recent run, to get *chainreader diagrams* for parity on a fast AWS machine.  
See [parity.md#run-18](../results/parity.md#run-18) for details. Almost identical to (D) above, just newer versions of some dependencies.

### (K) geth v1.8.14 on AWS t2.xlarge
Repeated recent run, to get *chainreader diagrams* for geth clique on a fast AWS machine. See [geth.md#run-2](geth.md#run-2) for details. Almost identical to (B), but without the ethstats docker instances.

Interesting new observation, now that I ran it for 50k transactions not 20k. See issue comment  https://github.com/ethereum/go-ethereum/issues/17447#issuecomment-431629285


### (L) IBFT quorum-crux on AWS t2.xlarge
Repeated recent run, to get *chainreader diagrams* for quorum IBFT on a fast AWS machine. See [quorum-IBFT.md#run-11](quorum-IBFT.md#run-11) for details. Almost identical to (F), so I don't know why it is suddenly 15% slower. 

Perhaps it is a newer version of quorum? Unfortunately I don't know as [quorum pretends to be geth](https://github.com/jpmorganchase/quorum/issues/507), and is stuck on version `Geth/v1.7.2` for a very long time now.


## you
Please inspire us what could make `parity aura` faster. 
Or actually ... what could make *any* of this faster. Thanks.

## issues
See bottom of [parity.md](../results/parity.md#issues), [geth.md](../results/geth.md#issues), 
[quorum.md](../results/quorum.md#issues-raised), [quorum-IBFT.md](../results/quorum-IBFT.md#issues).

