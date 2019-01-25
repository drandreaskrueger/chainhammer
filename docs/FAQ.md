# chainhammer FAQ
frequently asked questions, explaining approach, or code

TOC:

* detailed manual for installation & first run
  * install.sh 
  * initialization / preparation
  * run.sh quickstart script
* step-by-step manually: tps.py, deploy.py, send.py, ...
* gitlab private repo
* what if a script fails prematurely? Kill processes 
* docker problems? Kill & Remove docker containers
* web3 versus RPC

Also see [reproduce.md](reproduce.md), [cloud.md](cloud.md), and the per-client [results/*.md](results/) texts.

---

## how to install and run

step by step, in case the integrated script scripts/install.sh makes problems

### install.sh ALL dependencies 
New in v44: Installer for EVERYTHING that this repo needs!
```
cd chainhammer      # you must be in main folder
scripts/install.sh
```
but be CAREFUL: 
Better only use on a disposable/cloud/virtualbox machine, 
and NOT on your main work machine!!  

or 

only create the *virtualenv for the chainhammer Python programs*, then look into [scripts/install-virtualenv.sh](../scripts/install-virtualenv.sh)

(For more details see [reproduce.md](reproduce.md)).

### preparations

All python scripts & jupyer notebooks must be run *within that virtualenv*, e.g.:
```
cd hammer; source ../env/bin/activate
```
Now start your ethereum node(s), or simply: `source env/bin/activate; testrpc-py`

Before first ever run of chainhammer: 
```
touch account-passphrase.txt
./deploy.py andtests
```
It tests whether communication with the ethereum node is working, 
**and initially creates local files about the compiled and deployed contract**. 
If there are connection problems, check the ports in [config.py](hammer/config.py) --> 
`RPCaddress, RPCaddress2`.

### quickstart
A new integrated script which executes a lot of steps, one by one. Beware, this is still beta. Please report any issues, thanks.

    ./run.sh TestRPC-Local testrpc

or e.g.

    ./run.sh Geth-Clique-Local geth-clique

---

## alternatively: step-by-step manually
Remember, in each new terminal virtualenv: `cd hammer; source ../env/bin/activate`

first terminal:
```
./tps.py
```

second terminal:
```
./deploy.py; ./send.py 1000
```

Then, after all (e.g. 20,001) transactions have been seen, 
extract the whole chain into `parity-run17.db` (example);
and create the diagrams

```
cd ../reader
rm -f parity-run17.db*

./blocksDB_create.py parity-run17.db
./blocksDB_diagramming.py parity-run17.db Parity-run-17
```

---

## how to install from gitlab
More infos [here](https://stackoverflow.com/questions/30202642/how-can-i-clone-a-private-gitlab-repository).

Either
```
git clone https://gitlab.com/andreaskrueger/chainhammer andreaskrueger_chainhammer
cd andreaskrueger_chainhammer
```
with entering your gitlab username & password manually, or 


```
git clone git@gitlab.com:andreaskrueger/chainhammer andreaskrueger_chainhammer
cd andreaskrueger_chainhammer
```
when you have uploaded your .ssh key to gitlab. 

Then in both cases continue with install... in [README.md --> quickstart(../README.md#quickstart).


---

## what if a script fails prematurely?
Then there might be process running in the background, which prevent new runs, then this can be useful

    scripts/kill-leftovers.sh


---

## docker problems?

this is a very radical step, to kill & delete all docker images & containers:

    scripts/remove-all-docker.sh

---

## send via `web3.py` versus send via direct RPC call `eth_sendTransaction`
 
This question was asked here: https://github.com/paritytech/parity-ethereum/issues/9393#issuecomment-436294454

> because the web3 library is too slow

Yes, for low (two digit) TPS it does not make a big difference, only ~20% faster. But when I get into the hundreds of TPS, I see considerable gains (~twice as fast) when bypassing web3 completely.  Please have a quick look at these old experiments: https://github.com/drandreaskrueger/chainhammer/blob/master/log.md#sending-via-web3-versus-sending-via-rpc

When bypassing the web3.py library, I am using the RPC `method = 'eth_sendTransaction'` directly.

Have a look at these two codepieces:

### via web3  

in [contract_set_via_web3()](https://github.com/drandreaskrueger/chainhammer/blob/93c40384a4d178bdb00cea491d15b14046471b72/send.py#L73-L93) it is simply this one liner  
[`tx = contract.functions.set( x=arg ).transact(txParameters)`](https://github.com/drandreaskrueger/chainhammer/blob/93c40384a4d178bdb00cea491d15b14046471b72/send.py#L90)

while 

### via RPC

in [contract_set_via_RPC()](https://github.com/drandreaskrueger/chainhammer/blob/93c40384a4d178bdb00cea491d15b14046471b72/send.py#L106-L183),  
I am doing (`contract_method_ID()` + `arg` --> `argument_encoding()` --> `txParameters` --> `payload`), then (plus `headers` into a `requests.post()` to call the RPC endpoint `eth_sendTransaction`), see here:  
[`response = requests.post(RPCaddress, json=payload, headers=headers)`](https://github.com/drandreaskrueger/chainhammer/blob/93c40384a4d178bdb00cea491d15b14046471b72/send.py#L178)


### choice

I switch between those two routes here    
[`contrachow to install from gitlabt_set = contract_set_via_web3   if ROUTE=="web3" else contract_set_via_RPC`](https://github.com/drandreaskrueger/chainhammer/blob/93c40384a4d178bdb00cea491d15b14046471b72/send.py#L201)

choice constant `ROUTE` is defined in [`config.py`](https://github.com/drandreaskrueger/chainhammer/blob/93c40384a4d178bdb00cea491d15b14046471b72/config.py#L38)

I have now actually raised an 

### issue 
* [w3p#1133](https://github.com/ethereum/web3.py/issues/1133): *huge difference in TPS performance when bypassing web3.py in favor of a direct RPC call* 

---

## stuck during ./is_up.py

Can have many problems. 

First check this logfile:

    tail -n 10 -f logs/network.log

then try if you can connect to the node from the outside:

    geth attach http://localhost:8545

if the second fails, but the first looks good, 
I once on my local machine had an exotic problem 
with the **vpn** and the docker portmapping, 
then simply disconnecting from the vpn helped with that.

For more docker stuff, see below.


---

## docker

You could also try entering the :8545 container, 
and look into log files there.

    docker ps
    docker exec -it <hash> bash

perhaps prune the networks 

    docker network ls
    docker network prune

or restart the daemon?
    
    sudo service docker status
    sudo service docker restart
    sudo service docker status

---

## continue after errors / Ctrl-C

this script tries to kill as much as possible:

    scripts/kill-leftovers.sh

read it before you run it!

---

## out of memory

is hard to detect, so better have a terminal open with

    ssh chainhammer
    watch -n 10 "free -m"

you you can keep an eye on your RAM, and for your disk:

    watch -n 10 "df"


## Quorum off

Quorum-crux cannot run in a t2.micro with only 1 GB.  
To avoid problems, it is switched off by default.

Simply run with the switch $CH_QUORUM:

    CH_QUORUM=true CH_MACHINE=$HOSTNAME ./run-all_small.sh

if you want to enable it.
