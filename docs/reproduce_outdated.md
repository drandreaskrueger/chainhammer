
# chainhammer reproduce - outdated information
By version v54 of chainhammer, a lot here is automated much more, so much here is not needed anymore, because it is scripted. 

However, some of these tutorials might still be useful for running some experiments or tests manually, so ... keeping them for now.

TODO: Sort them into the per-client-infofiles.


## How to replicate the results
quickstart --> **Scroll down to the AWS chapter.**

### dockerized parity network
```
# parity-deploy.sh
# for a dockerized parity environment
# this is instantseal, NOT a realistic network of nodes
# but it already shows the problem - parity is very slow.
# For a more realistic network of 4 aura nodes see chainhammer-->parity.md

cd paritytech_parity-deploy
sudo ./clean.sh
./parity-deploy.sh --config dev --name instantseal --geth
docker-compose up
```
That starts one `instantseal` node - but that already shows that parity cannot get faster than ~70 TPS. Use this for now.

(Later, you can try `aura` networks of 4 nodes instead - see instructions 
here: [parity.md --> run 13](../results/parity.md#run-13) )


### chainhammer
new terminal:
```
# configure chainhammer
nano config.py

RPCaddress, RPCaddress2 = 'http://localhost:8545', 'http://localhost:8545'
ROUTE = "web3"
```

```
# test connection
touch account-passphrase.txt
./deploy.py 
```

```
# start the chainhammer viewer
./tps.py
```

new terminal


```
# same virtualenv
cd drandreaskrueger_chainhammer
source env/bin/activate

#### start the chainhammer send routine
./deploy.py notest; ./send.py 
```

or:

```
# not blocking but with 23 multi-threading workers
./deploy.py notest; ./send.py threaded2 23
```
---

### everything below here is *not necessary*
... to improve **parity**'s speed.

(but it provides a local `geth` installation, for `geth attach http://localhost:8545`)

new terminal

( * )

```
# check that the transactions are actually successfully executed:

geth attach http://localhost:8545

> web3.eth.getTransaction(web3.eth.getBlock(50)["transactions"][0])
{
  gas: 90000, ...
}

> web3.eth.getTransactionReceipt(web3.eth.getBlock(50)["transactions"][0])
{ 
  gasUsed: 26691,
  status: "0x1", ...
}
> 
```

### geth - dockerized: please help

( * ) I actually do *not* want to install `geth` locally, but start the geth console *from a docker container* - but no success yet:

```
docker run ethereum/client-go attach https://localhost:8545
```
> WARN [09-10|09:38:24.984] Sanitizing cache to Go's GC limits       provided=1024 updated=331  
> Fatal: Failed to start the JavaScript console: api modules: Post https://localhost:8545: dial tcp 127.0.0.1:8545: connect: connection refused  
> Fatal: Failed to start the JavaScript console: api modules: Post https://localhost:8545: dial tcp 127.0.0.1:8545: connect: connection refused  

Please help me with ^ this, thanks.

...

Until that is sorted, I have simply installed `geth` *locally*, see  `install.sh` --> `install-geth.sh`


### geth clique
Compare the poor TPS performance of `parity aura` with the faster `geth clique`:

#### stop parity
Kill the above `parity-deploy.sh ...; docker-compose up` with:

Ctrl-C, then

```
docker-compose down -v
```
you might run out of disk space, so better delete any docker stuff:
```
docker kill $(docker ps -q) ; docker rm $(docker ps -a -q) ; docker rmi $(docker images -q)
```

#### geth Clique network with dockerized nodes
for details see [geth.md#javahippiegetset +xh-dev](https://github.com/drandreaskrueger/chainhammer/blob/0bdcbedfeeb261c534ae3baeb0bd9a37054c9b28/geth.md#javahippiegeth-dev).

```
cd drandreaskrueger_geth-dev

docker-compose up
```
wait until you see healthy looking logging, like

```
monitor-frontend         | 2018-09-10 13:34:02.054 [API] [BLK] Block: 7 from: gethDev1
```

##### start benchmark

new terminal: test connection
```
cd drandreaskrueger_chainhammer/
source env/bin/activate
./deploy.py
```


new terminal: watcher
```
cd drandreaskrueger_chainhammer/
source env/bin/activate
./tps.py
```

new terminal: hammer
```
cd drandreaskrueger_chainhammer/
source env/bin/activate
./deploy.py notest; ./send.py 
```


### quorum-crux-IBFT

A dockerized quorum-crux network of 4 nodes using IBFT (*Istanbul Byzantine Fault Tolerance*) consensus:

#### local build

Edit the given `blk-io/crux`, so that it builds a local docker container, instead of using `blkio10/quorum-crux:v1.0.0` from dockerhub:

```
cd blk-io_crux/docker/quorum-crux/
cp docker-compose.yaml docker-compose-local.yaml

nano docker-compose-local.yaml 
```
Follow the instructions "to build the Docker images yourself", so that it looks like this:
```
...
  node1: &quorum_crux_node
    # Pull image down from Docker Hub
    # image: blkio10/quorum-crux:v1.0.0
    # Uncomment the below, and comment out the above line to build the Docker images yourself
    image: blk.io/quorum/quorum-crux
    build:
      context: .
    container_name: quorum1
...
```

#### TPS-optimized network settings 

Edit the settings: Higher gas limit, larger txpool, blockperiod 1 second
```
sudo apt install jq
jq '.gasLimit = "0x1312D00"' istanbul-genesis.json > tmp && mv tmp istanbul-genesis.json

sed -i 's/PRIVATE_CONFIG/ARGS=$ARGS"--txpool.globalslots 20000 --txpool.globalqueue 20000 --istanbul.blockperiod 1 "\nPRIVATE_CONFIG/g' istanbul-start.sh 
```

#### build and start
then build the container, and start the network:
```
docker-compose -f docker-compose-local.yaml up --build
```

wait until you see something like

```
...
quorum1  | [*] Starting Crux nodes
quorum3  | [*] Starting Ethereum nodes
...
quorum1  | set +v
```



### parity
```
ssh chainhammer

cd ~/paritytech_parity-deploy
# sed -i 's/0x1312D00/0x2625A00/g' config/spec/genesis/aura; cat config/spec/genesis/aura # hardcoded now in parity-deploy https://github.com/paritytech/parity-deploy/issues/55#issuecomment-422309365

ARGS="--db-compaction ssd --tracing off --gasprice 0 --gas-floor-target 100000000000 "
ARGS=$ARGS"--pruning fast --tx-queue-size 32768 --tx-queue-mem-limit 0 --no-warp "
ARGS=$ARGS"--jsonrpc-threads 8 --no-hardware-wallets --no-dapps --no-secretstore-http "
ARGS=$ARGS"--cache-size 4096 --scale-verifiers --num-verifiers 16 --force-sealing "

sudo ./clean.sh 
./parity-deploy.sh --nodes 4 --config aura --name myaura --geth $ARGS

sed -i 's/parity:stable/parity:v1.11.11/g' docker-compose.yml
jq ".engine.authorityRound.params.stepDuration = 5" deployment/chain/spec.json > tmp; mv tmp deployment/chain/spec.json

cp ~/paritytech_parity-deploy/deployment/1/password ~/drandreaskrueger_chainhammer/account-passphrase.txt
docker-compose up
```
For explanations of all those settings, see [parity.md](../results/parity.md). 

If you later want to end this ... 'Ctrl-c' and:

```
docker-compose down -v
sudo ./clean.sh
```

or even
```
~/remove-all-docker.sh docker-compose -f docker-compose-local.yaml up --build
```

### geth

```
ssh chainhammer

cd ~/drandreaskrueger_geth-dev/
docker-compose up
```

If you want to end this ... 'Ctrl-c' and:

```
docker-compose down -v
```

### quorum-crux IBFT

```
ssh chainhammer
```

note the `-local` in the docker-compose command! -->
```
cd ~/blk-io_crux/docker/quorum-crux/
docker-compose -f docker-compose-local.yaml up --build
```

If you want to end this ... 'Ctrl-c' and:

```
docker-compose -f docker-compose-local.yaml down -v
```

and possibly destroy all docker
```
~/remove-all-docker.sh
```

N.B.: Port is changed from 8545 to 22001:

```
nano ~/drandreaskrueger_chainhammer/config.py
```
change to
```
RPCaddress, RPCaddress2 = 'http://localhost:22001', 'http://localhost:22002'
```
##### careful
Until `blk-io/crux` have also included a [docker-compose-local.yaml](#local-build) into their own repo, pay attention whether the two .yaml are still in sync:
```
diff docker-compose-local.yaml docker-compose.yaml
```

### chainhammer: test connection
... and create some local files
```
ssh chainhammer
cd ~/drandreaskrueger_chainhammer && source env/bin/activate

./deploy.py
```
If there are connection problems, probably need to configure the correct ports 
in [config.py](../hammer/config.py):
```
nano config.py
```
or set the correct account passphrase:
```
cp ~/paritytech_parity-deploy/deployment/1/password ~/drandreaskrueger_chainhammer/account-passphrase.txt
```


### chainhammer: watcher
```
./tps.py
```

### chainhammer: send transactions
```
ssh chainhammer
cd drandreaskrueger_chainhammer && source env/bin/activate

./deploy.py notest; ./send.py threaded2 23
```

## issues
See bottom of [parity.md](../results/parity.md#issues), [geth.md](../results/geth.md#issues), 
[quorum.md](../results/quorum.md#issues-raised), [quorum-IBFT.md](../results/quorum-IBFT.md#issues).

