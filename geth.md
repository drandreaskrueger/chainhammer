# geth Clique PoA benchmarking
To have a nodes setup comparable to the  quorum [7nodes example](https://github.com/jpmorganchase/quorum-examples/tree/master/examples/7nodes) or the blk.io [crux-quorum-4nodes-docker-compose](https://github.com/blk-io/crux/blob/master/docker/quorum-crux/docker-compose.yaml), I am looking for a dockerized or vagrant virtualbox. Please tell me if you know a good one. For now I have chosen

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

N.B.: Whenever changing those parameters, I am brutally killing all docker images, for better ways see [this issue](https://github.com/javahippie/geth-dev/issues/15).

## results
...

## issues
* [GD#13](https://github.com/javahippie/geth-dev/issues/13) chain is stuck at block 1 or block 2
* [GD#14](https://github.com/javahippie/geth-dev/issues/14) account password?
* [GD#15](https://github.com/javahippie/geth-dev/issues/15) remove chain without rebuilding whole container 