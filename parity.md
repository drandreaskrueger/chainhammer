# parity PoA benchmarking

## parity docker
Following informative wiki page https://github.com/paritytech/wiki/blob/master/Docker.md

Initial -brutal- cleaning of my machine:
```
docker rm $(docker ps -a -q); docker rmi $(docker images -q)
```

### dockerized paritytech/parity-ethereum v1.11.8 

The newest stable [release](https://github.com/paritytech/parity-ethereum/releases) v1.11.8 does exist as a docker image on dockerhub:

```
curl -sS 'https://registry.hub.docker.com/v2/repositories/parity/parity/tags/'  | jq '."results"[]["name"]' | sort

"beta"
"gitlab-next"
"latest"
"nightly"
"stable"
"v1.11.8"
"v2.0.0"
"v2.0.1"
"v2.1.0-rc1"
"v2.1.0-rc2"
```

run

    docker run -ti parity/parity:v1.11.8


#### configure

    docker run -ti parity/parity:v1.11.8 --help


run with open ports

    docker run -ti -p 8180:8180 -p 8545:8545 -p 8546:8546 -p 30303:30303 -p 30303:30303/udp parity/parity:v1.11.8 --ui-interface all --jsonrpc-interface all

perhaps useful: [Parity Config Generator](https://paritytech.github.io/parity-config-generator/)

then 

    docker run -ti -v ~/.local/share/io.parity.ethereum/docker/:/root/.local/share/io.parity.ethereum/ parity/parity:v1.11.8 --config /root/.local/share/io.parity.ethereum/config.toml

### parity-deploy = docker-compose generator tool

https://github.com/paritytech/parity-deploy

example

    ./parity-deploy.sh --config aura --name parity_my-aura --nodes 4 --ethstats
    docker-compose up


that tool looks really promising. But it results in a non-functioning `docker-compose.yml` - see [PD#51](https://github.com/paritytech/parity-deploy/issues/51)

aborting this for now.

### orbita-center/parity-poa-playground
> Parity PoA network with 3 authorities and 3 members.

```
git clone https://github.com/orbita-center/parity-poa-playground orbita-center_parity-poa-playground
cd orbita-center_parity-poa-playground
docker-compose up
```
#### good first impression:
* http://localhost:3001/ comes up, with 3 authorities, and 3 members
* port 8545 is answering:

```
curl -X POST --data '{"jsonrpc":"2.0","method":"net_version","params":[],"id":67}' -H "Content-Type: application/json" localhost:8545
{"jsonrpc":"2.0","result":"8995","id":67}
```

#### modify 

only 1 change needed: Add geth compatibility mode (needed e.g. for timed unlocking of accounts)

    --geth

before line 13 in https://github.com/orbita-center/parity-poa-playground/blob/master/docker-compose.yml#L12-L13

more modifications = scroll further down

#### my fork of parity-poa-playground

https://github.com/drandreaskrueger/parity-poa-playground

## benchmarking

### chainhammer settings 

#### config.py

    RPCaddress, RPCaddress2 = 'http://localhost:8545', 'http://localhost:8545' 
    RAFT = False
    ROUTE = "RPC"  

#### account-passphrase.txt

empty file


### initial run, unoptimized

Before [PPP#14](https://github.com/orbita-center/parity-poa-playground/issues/14) was answered, with "out of the box" chain.json settings, and no tweaks ... we see mediocre results initially:

#### log of run 1

```
./tps.py 

versions: web3 4.3.0, py-solc: 2.1.0, solc 0.4.23+commit.124ca40d.Linux.gpp, testrpc 1.3.4, python 3.5.3 (default, Jan 19 2017, 14:11:04) [GCC 6.3.0 20170118]
web3 connection established, blockNumber = 106, node version string =  Parity//v1.11.8-stable-92776e4-20180728/x86_64-linux-gnu/rustc1.27.2
first account of node is 0x000a3702732843418D83A03E65A3d9f7aDd58864, balance is 10000000000 Ether
nodeName: Parity, nodeType: Parity, consensus: ???, chainName: parity-poa-playground

Block  106  - waiting for something to happen
(filedate 1534862035) last contract address: 0xBD45194215D595444c07A591A9D6E5a1fA53f169
(filedate 1534863468) new contract address: 0x02615cCb36C65E120C3598aba61eB455Cf18A578

starting timer, at block 108 which has  1  transactions; at timecode 24644.527843475
block 108 | new #TX 144 / 3000 ms =  48.0 TPS_current | total: #TX  145 /  2.8 s =  51.9 TPS_average
block 109 | new #TX 198 / 3000 ms =  66.0 TPS_current | total: #TX  343 /  5.8 s =  58.7 TPS_average
block 110 | new #TX 194 / 3000 ms =  64.7 TPS_current | total: #TX  537 /  8.9 s =  60.4 TPS_average
block 111 | new #TX 179 / 3000 ms =  59.7 TPS_current | total: #TX  716 / 11.9 s =  60.0 TPS_average
block 112 | new #TX 189 / 3000 ms =  63.0 TPS_current | total: #TX  905 / 14.7 s =  61.6 TPS_average
block 113 | new #TX 194 / 3000 ms =  64.7 TPS_current | total: #TX 1099 / 17.8 s =  61.9 TPS_average
block 114 | new #TX 194 / 3000 ms =  64.7 TPS_current | total: #TX 1293 / 20.8 s =  62.1 TPS_average
block 115 | new #TX 186 / 3000 ms =  62.0 TPS_current | total: #TX 1479 / 23.9 s =  62.0 TPS_average
block 116 | new #TX 196 / 3000 ms =  65.3 TPS_current | total: #TX 1675 / 26.9 s =  62.2 TPS_average
block 117 | new #TX 193 / 3000 ms =  64.3 TPS_current | total: #TX 1868 / 30.0 s =  62.3 TPS_average
block 118 | new #TX 196 / 3000 ms =  65.3 TPS_current | total: #TX 2064 / 33.0 s =  62.5 TPS_average
block 119 | new #TX 183 / 3000 ms =  61.0 TPS_current | total: #TX 2247 / 35.8 s =  62.8 TPS_average
block 120 | new #TX 198 / 3000 ms =  66.0 TPS_current | total: #TX 2445 / 38.8 s =  63.0 TPS_average
block 121 | new #TX 196 / 3000 ms =  65.3 TPS_current | total: #TX 2641 / 41.9 s =  63.0 TPS_average
block 122 | new #TX 184 / 3000 ms =  61.3 TPS_current | total: #TX 2825 / 45.0 s =  62.8 TPS_average
block 123 | new #TX  26 / 2000 ms =  13.0 TPS_current | total: #TX 2851 / 46.8 s =  60.9 TPS_average
block 124 | new #TX   5 / 2000 ms =   2.5 TPS_current | total: #TX 2856 / 48.9 s =  58.4 TPS_average
block 125 | new #TX 550 / 5000 ms = 110.0 TPS_current | total: #TX 3406 / 53.8 s =  63.3 TPS_average
block 126 | new #TX 184 / 3000 ms =  61.3 TPS_current | total: #TX 3590 / 56.9 s =  63.1 TPS_average
block 127 | new #TX   6 / 2000 ms =   3.0 TPS_current | total: #TX 3596 / 59.0 s =  60.9 TPS_average
block 128 | new #TX   3 / 3000 ms =   1.0 TPS_current | total: #TX 3599 / 62.0 s =  58.0 TPS_average
block 129 | new #TX  83 / 3000 ms =  27.7 TPS_current | total: #TX 3682 / 65.1 s =  56.6 TPS_average
block 130 | new #TX   2 / 5000 ms =   0.4 TPS_current | total: #TX 3684 / 69.9 s =  52.7 TPS_average
block 131 | new #TX 1086 / 5000 ms = 217.2 TPS_current | total: #TX 4770 / 75.1 s =  63.5 TPS_average
block 132 | new #TX 171 / 3000 ms =  57.0 TPS_current | total: #TX 4941 / 77.9 s =  63.4 TPS_average
block 133 | new #TX 197 / 3000 ms =  65.7 TPS_current | total: #TX 5138 / 81.0 s =  63.5 TPS_average
block 134 | new #TX 183 / 3000 ms =  61.0 TPS_current | total: #TX 5321 / 83.7 s =  63.6 TPS_average
block 135 | new #TX 191 / 3000 ms =  63.7 TPS_current | total: #TX 5512 / 86.8 s =  63.5 TPS_average
block 136 | new #TX 194 / 3000 ms =  64.7 TPS_current | total: #TX 5706 / 89.8 s =  63.5 TPS_average
block 137 | new #TX 184 / 3000 ms =  61.3 TPS_current | total: #TX 5890 / 92.9 s =  63.4 TPS_average
block 138 | new #TX 197 / 3000 ms =  65.7 TPS_current | total: #TX 6087 / 95.9 s =  63.4 TPS_average
block 139 | new #TX 191 / 3000 ms =  63.7 TPS_current | total: #TX 6278 / 99.0 s =  63.4 TPS_average
block 140 | new #TX 179 / 3000 ms =  59.7 TPS_current | total: #TX 6457 / 101.8 s =  63.5 TPS_average
block 141 | new #TX 186 / 3000 ms =  62.0 TPS_current | total: #TX 6643 / 104.8 s =  63.4 TPS_average
block 142 | new #TX 192 / 3000 ms =  64.0 TPS_current | total: #TX 6835 / 107.9 s =  63.3 TPS_average
block 143 | new #TX 171 / 3000 ms =  57.0 TPS_current | total: #TX 7006 / 110.9 s =  63.1 TPS_average
block 144 | new #TX 197 / 3000 ms =  65.7 TPS_current | total: #TX 7203 / 114.0 s =  63.2 TPS_average
block 145 | new #TX 197 / 3000 ms =  65.7 TPS_current | total: #TX 7400 / 117.0 s =  63.2 TPS_average
block 146 | new #TX 194 / 3000 ms =  64.7 TPS_current | total: #TX 7594 / 120.1 s =  63.2 TPS_average
block 147 | new #TX 191 / 3000 ms =  63.7 TPS_current | total: #TX 7785 / 122.9 s =  63.4 TPS_average
block 148 | new #TX 189 / 3000 ms =  63.0 TPS_current | total: #TX 7974 / 125.9 s =  63.3 TPS_average
block 149 | new #TX   1 / 2000 ms =   0.5 TPS_current | total: #TX 7975 / 128.1 s =  62.3 TPS_average
block 150 | new #TX   2 / 2000 ms =   1.0 TPS_current | total: #TX 7977 / 129.9 s =  61.4 TPS_average
block 151 | new #TX   3 / 3000 ms =   1.0 TPS_current | total: #TX 7980 / 132.9 s =  60.0 TPS_average
block 152 | new #TX   1 / 3000 ms =   0.3 TPS_current | total: #TX 7981 / 135.7 s =  58.8 TPS_average
block 153 | new #TX 784 / 2000 ms = 392.0 TPS_current | total: #TX 8765 / 137.9 s =  63.6 TPS_average
block 154 | new #TX 193 / 3000 ms =  64.3 TPS_current | total: #TX 8958 / 140.9 s =  63.6 TPS_average
block 155 | new #TX 186 / 3000 ms =  62.0 TPS_current | total: #TX 9144 / 144.0 s =  63.5 TPS_average
block 156 | new #TX 192 / 3000 ms =  64.0 TPS_current | total: #TX 9336 / 146.7 s =  63.6 TPS_average
block 157 | new #TX   2 / 2000 ms =   1.0 TPS_current | total: #TX 9338 / 148.8 s =  62.7 TPS_average
block 158 | new #TX  51 / 3000 ms =  17.0 TPS_current | total: #TX 9389 / 151.9 s =  61.8 TPS_average
block 159 | new #TX 103 / 3000 ms =  34.3 TPS_current | total: #TX 9492 / 154.9 s =  61.3 TPS_average
block 160 | new #TX   9 / 3000 ms =   3.0 TPS_current | total: #TX 9501 / 158.0 s =  60.1 TPS_average
block 161 | new #TX 163 / 3000 ms =  54.3 TPS_current | total: #TX 9664 / 161.0 s =  60.0 TPS_average
block 162 | new #TX 1064 / 7000 ms = 152.0 TPS_current | total: #TX 10728 / 168.0 s =  63.9 TPS_average
block 163 | new #TX 179 / 3000 ms =  59.7 TPS_current | total: #TX 10907 / 171.1 s =  63.8 TPS_average
block 164 | new #TX 201 / 3000 ms =  67.0 TPS_current | total: #TX 11108 / 174.1 s =  63.8 TPS_average
block 165 | new #TX 184 / 3000 ms =  61.3 TPS_current | total: #TX 11292 / 176.8 s =  63.9 TPS_average
block 166 | new #TX  60 / 2000 ms =  30.0 TPS_current | total: #TX 11352 / 179.0 s =  63.4 TPS_average
block 167 | new #TX   5 / 2000 ms =   2.5 TPS_current | total: #TX 11357 / 181.1 s =  62.7 TPS_average
block 168 | new #TX 524 / 5000 ms = 104.8 TPS_current | total: #TX 11881 / 186.0 s =  63.9 TPS_average
block 169 | new #TX 189 / 3000 ms =  63.0 TPS_current | total: #TX 12070 / 188.8 s =  63.9 TPS_average
block 170 | new #TX  45 / 2000 ms =  22.5 TPS_current | total: #TX 12115 / 190.9 s =  63.5 TPS_average
block 171 | new #TX   8 / 3000 ms =   2.7 TPS_current | total: #TX 12123 / 193.9 s =  62.5 TPS_average
block 172 | new #TX  12 / 3000 ms =   4.0 TPS_current | total: #TX 12135 / 197.0 s =  61.6 TPS_average
block 173 | new #TX  69 / 2000 ms =  34.5 TPS_current | total: #TX 12204 / 199.1 s =  61.3 TPS_average
block 174 | new #TX  14 / 3000 ms =   4.7 TPS_current | total: #TX 12218 / 202.1 s =  60.5 TPS_average
block 175 | new #TX  17 / 3000 ms =   5.7 TPS_current | total: #TX 12235 / 204.9 s =  59.7 TPS_average
block 176 | new #TX 163 / 3000 ms =  54.3 TPS_current | total: #TX 12398 / 207.9 s =  59.6 TPS_average
block 177 | new #TX 1253 / 5000 ms = 250.6 TPS_current | total: #TX 13651 / 213.1 s =  64.1 TPS_average
block 178 | new #TX 171 / 3000 ms =  57.0 TPS_current | total: #TX 13822 / 215.9 s =  64.0 TPS_average
block 179 | new #TX 200 / 3000 ms =  66.7 TPS_current | total: #TX 14022 / 218.9 s =  64.0 TPS_average
block 180 | new #TX 200 / 3000 ms =  66.7 TPS_current | total: #TX 14222 / 222.0 s =  64.1 TPS_average
block 181 | new #TX 189 / 3000 ms =  63.0 TPS_current | total: #TX 14411 / 225.0 s =  64.0 TPS_average
block 182 | new #TX 192 / 3000 ms =  64.0 TPS_current | total: #TX 14603 / 227.8 s =  64.1 TPS_average
block 183 | new #TX  46 / 2000 ms =  23.0 TPS_current | total: #TX 14649 / 229.9 s =  63.7 TPS_average
block 184 | new #TX 163 / 3000 ms =  54.3 TPS_current | total: #TX 14812 / 233.0 s =  63.6 TPS_average
block 185 | new #TX  81 / 3000 ms =  27.0 TPS_current | total: #TX 14893 / 236.0 s =  63.1 TPS_average
block 186 | new #TX   3 / 3000 ms =   1.0 TPS_current | total: #TX 14896 / 239.0 s =  62.3 TPS_average
block 187 | new #TX  78 / 3000 ms =  26.0 TPS_current | total: #TX 14974 / 241.8 s =  61.9 TPS_average
block 188 | new #TX  13 / 3000 ms =   4.3 TPS_current | total: #TX 14987 / 244.8 s =  61.2 TPS_average
block 189 | new #TX  69 / 3000 ms =  23.0 TPS_current | total: #TX 15056 / 247.9 s =  60.7 TPS_average
block 190 | new #TX   7 / 3000 ms =   2.3 TPS_current | total: #TX 15063 / 250.9 s =  60.0 TPS_average
block 191 | new #TX   1 / 3000 ms =   0.3 TPS_current | total: #TX 15064 / 253.9 s =  59.3 TPS_average
block 192 | new #TX 155 / 2000 ms =  77.5 TPS_current | total: #TX 15219 / 256.1 s =  59.4 TPS_average
block 193 | new #TX 1349 / 2000 ms = 674.5 TPS_current | total: #TX 16568 / 258.0 s =  64.2 TPS_average
block 194 | new #TX 177 / 3000 ms =  59.0 TPS_current | total: #TX 16745 / 261.1 s =  64.1 TPS_average
block 195 | new #TX 184 / 3000 ms =  61.3 TPS_current | total: #TX 16929 / 263.8 s =  64.2 TPS_average
block 196 | new #TX 201 / 3000 ms =  67.0 TPS_current | total: #TX 17130 / 266.9 s =  64.2 TPS_average
block 197 | new #TX  48 / 2000 ms =  24.0 TPS_current | total: #TX 17178 / 269.0 s =  63.9 TPS_average
block 198 | new #TX  28 / 5000 ms =   5.6 TPS_current | total: #TX 17206 / 273.8 s =  62.8 TPS_average
block 199 | new #TX 517 / 2000 ms = 258.5 TPS_current | total: #TX 17723 / 276.0 s =  64.2 TPS_average
block 200 | new #TX 187 / 3000 ms =  62.3 TPS_current | total: #TX 17910 / 279.1 s =  64.2 TPS_average
block 201 | new #TX 198 / 3000 ms =  66.0 TPS_current | total: #TX 18108 / 282.1 s =  64.2 TPS_average
block 202 | new #TX 196 / 3000 ms =  65.3 TPS_current | total: #TX 18304 / 284.9 s =  64.2 TPS_average
block 203 | new #TX 188 / 3000 ms =  62.7 TPS_current | total: #TX 18492 / 288.0 s =  64.2 TPS_average
block 204 | new #TX 197 / 3000 ms =  65.7 TPS_current | total: #TX 18689 / 291.0 s =  64.2 TPS_average
block 205 | new #TX 197 / 3000 ms =  65.7 TPS_current | total: #TX 18886 / 294.1 s =  64.2 TPS_average
block 206 | new #TX 183 / 3000 ms =  61.0 TPS_current | total: #TX 19069 / 296.8 s =  64.2 TPS_average
block 207 | new #TX  39 / 2000 ms =  19.5 TPS_current | total: #TX 19108 / 298.9 s =  63.9 TPS_average
block 208 | new #TX 549 / 7000 ms =  78.4 TPS_current | total: #TX 19657 / 305.9 s =  64.3 TPS_average
block 209 | new #TX 196 / 3000 ms =  65.3 TPS_current | total: #TX 19853 / 309.0 s =  64.3 TPS_average
block 210 | new #TX  11 / 2000 ms =   5.5 TPS_current | total: #TX 19864 / 311.1 s =  63.8 TPS_average
block 211 | new #TX 137 / 6000 ms =  22.8 TPS_current | total: #TX 20001 / 317.0 s =  63.1 TPS_average
block 212 | new #TX   0 / 77000 ms =   0.0 TPS_current | total: #TX 20001 / 393.9 s =  50.8 TPS_average
block 213 | new #TX   0 / 38000 ms =   0.0 TPS_current | total: #TX 20001 / 431.9 s =  46.3 TPS_average
block 214 | new #TX   0 / 11000 ms =   0.0 TPS_current | total: #TX 20001 / 442.9 s =  45.2 TPS_average
block 215 | new #TX   0 / 74000 ms =   0.0 TPS_current | total: #TX 20001 / 517.1 s =  38.7 TPS_average
```

#### result initial run1: > 60 TPS

![chainreader/img/parity-poa-playground_run1_tps-bt-bs-gas_blks108-211.png](chainreader/img/parity-poa-playground_run1_tps-bt-bs-gas_blks108-211.png)



### run2
With [these altered settings](https://github.com/drandreaskrueger/parity-poa-playground/commit/d4c1aa3fc504e940a5a2f56de62f8a62734b2f8d)

```
      --jsonrpc-server-threads 8
      --tx-queue-size 16536
      --scale-verifiers
```
it's worse:

```
./tps.py 
versions: web3 4.3.0, py-solc: 2.1.0, solc 0.4.23+commit.124ca40d.Linux.gpp, testrpc 1.3.4, python 3.5.3 (default, Jan 19 2017, 14:11:04) [GCC 6.3.0 20170118]
web3 connection established, blockNumber = 0, node version string =  Parity//v1.11.8-stable-92776e4-20180728/x86_64-linux-gnu/rustc1.27.2
first account of node is 0x000a3702732843418D83A03E65A3d9f7aDd58864, balance is 10000000000 Ether
nodeName: Parity, nodeType: Parity, consensus: ???, network: 8995, chainName: parity-poa-playground, chainId: 8995

Block  0  - waiting for something to happen
(filedate 1535544939) last contract address: 0x536A0b91265dE1Ce1Ba541e54874AC21eC0E63e6
(filedate 1535545118) new contract address: 0x536A0b91265dE1Ce1Ba541e54874AC21eC0E63e6

starting timer, at block 1 which has  1  transactions; at timecode 45801.661595177
block 1 | new #TX  12 / 3000 ms =   4.0 TPS_current | total: #TX   13 /  2.7 s =   4.7 TPS_average
block 2 | new #TX 385 / 4000 ms =  96.2 TPS_current | total: #TX  398 /  7.0 s =  56.9 TPS_average
block 3 | new #TX 182 / 3000 ms =  60.7 TPS_current | total: #TX  580 / 10.1 s =  57.7 TPS_average
block 4 | new #TX 192 / 3000 ms =  64.0 TPS_current | total: #TX  772 / 13.1 s =  58.9 TPS_average
block 5 | new #TX 186 / 3000 ms =  62.0 TPS_current | total: #TX  958 / 15.9 s =  60.4 TPS_average
block 6 | new #TX 187 / 3000 ms =  62.3 TPS_current | total: #TX 1145 / 18.9 s =  60.5 TPS_average
block 7 | new #TX 195 / 3000 ms =  65.0 TPS_current | total: #TX 1340 / 22.0 s =  61.0 TPS_average
block 8 | new #TX 181 / 3000 ms =  60.3 TPS_current | total: #TX 1521 / 24.7 s =  61.6 TPS_average
block 9 | new #TX  50 / 2000 ms =  25.0 TPS_current | total: #TX 1571 / 26.8 s =  58.5 TPS_average
block 10 | new #TX  86 / 3000 ms =  28.7 TPS_current | total: #TX 1657 / 29.9 s =  55.5 TPS_average
block 11 | new #TX   8 / 3000 ms =   2.7 TPS_current | total: #TX 1665 / 32.9 s =  50.6 TPS_average
block 12 | new #TX  73 / 2000 ms =  36.5 TPS_current | total: #TX 1738 / 35.1 s =  49.6 TPS_average
block 13 | new #TX 163 / 7000 ms =  23.3 TPS_current | total: #TX 1901 / 42.1 s =  45.2 TPS_average
block 14 | new #TX  81 / 3000 ms =  27.0 TPS_current | total: #TX 1982 / 44.8 s =  44.2 TPS_average
block 15 | new #TX  81 / 8000 ms =  10.1 TPS_current | total: #TX 2063 / 53.0 s =  38.9 TPS_average
block 16 | new #TX 1779 / 8000 ms = 222.4 TPS_current | total: #TX 3842 / 61.0 s =  63.0 TPS_average
block 17 | new #TX 163 / 3000 ms =  54.3 TPS_current | total: #TX 4005 / 63.8 s =  62.8 TPS_average
block 18 | new #TX 192 / 3000 ms =  64.0 TPS_current | total: #TX 4197 / 66.9 s =  62.8 TPS_average
block 19 | new #TX 183 / 3000 ms =  61.0 TPS_current | total: #TX 4380 / 69.9 s =  62.7 TPS_average
block 20 | new #TX 183 / 3000 ms =  61.0 TPS_current | total: #TX 4563 / 73.0 s =  62.5 TPS_average
block 21 | new #TX 182 / 3000 ms =  60.7 TPS_current | total: #TX 4745 / 75.7 s =  62.6 TPS_average
block 22 | new #TX 187 / 3000 ms =  62.3 TPS_current | total: #TX 4932 / 78.8 s =  62.6 TPS_average
block 23 | new #TX 192 / 3000 ms =  64.0 TPS_current | total: #TX 5124 / 81.9 s =  62.6 TPS_average
block 24 | new #TX 184 / 3000 ms =  61.3 TPS_current | total: #TX 5308 / 84.9 s =  62.5 TPS_average
block 25 | new #TX 180 / 3000 ms =  60.0 TPS_current | total: #TX 5488 / 87.7 s =  62.6 TPS_average
block 26 | new #TX  12 / 2000 ms =   6.0 TPS_current | total: #TX 5500 / 89.9 s =  61.2 TPS_average
block 27 | new #TX   4 / 3000 ms =   1.3 TPS_current | total: #TX 5504 / 92.9 s =  59.2 TPS_average
block 28 | new #TX 163 / 3000 ms =  54.3 TPS_current | total: #TX 5667 / 95.9 s =  59.1 TPS_average
block 29 | new #TX   3 / 3000 ms =   1.0 TPS_current | total: #TX 5670 / 98.7 s =  57.5 TPS_average
block 30 | new #TX 144 / 3000 ms =  48.0 TPS_current | total: #TX 5814 / 102.0 s =  57.0 TPS_average
block 31 | new #TX   0 / 74000 ms =   0.0 TPS_current | total: #TX 5814 / 175.6 s =  33.1 TPS_average
block 32 | new #TX   0 / 32000 ms =   0.0 TPS_current | total: #TX 5814 / 207.9 s =  28.0 TPS_average
block 33 | new #TX   0 / 17000 ms =   0.0 TPS_current | total: #TX 5814 / 224.9 s =  25.9 TPS_average
block 34 | new #TX   0 / 71000 ms =   0.0 TPS_current | total: #TX 5814 / 295.8 s =  19.7 TPS_average
block 35 | new #TX   0 / 35000 ms =   0.0 TPS_current | total: #TX 5814 / 331.1 s =  17.6 TPS_average
block 36 | new #TX   0 / 20000 ms =   0.0 TPS_current | total: #TX 5814 / 350.9 s =  16.6 TPS_average
block 37 | new #TX   0 / 68000 ms =   0.0 TPS_current | total: #TX 5814 / 418.7 s =  13.9 TPS_average
block 38 | new #TX   0 / 38000 ms =   0.0 TPS_current | total: #TX 5814 / 456.9 s =  12.7 TPS_average
block 39 | new #TX   0 / 17000 ms =   0.0 TPS_current | total: #TX 5814 / 474.0 s =  12.3 TPS_average
```
Speed is not higher, but over 14000 transactions are lost !!

### run3
When [omitting the](https://github.com/drandreaskrueger/parity-poa-playground/commit/788eba40acbbeb71c459bc4237b3004d3c4ff2a7)

          --scale-verifiers
          
it looks better.

Not fast - but at least not losing transactions anymore:

```
./tps.py 
versions: web3 4.3.0, py-solc: 2.1.0, solc 0.4.23+commit.124ca40d.Linux.gpp, testrpc 1.3.4, python 3.5.3 (default, Jan 19 2017, 14:11:04) [GCC 6.3.0 20170118]
web3 connection established, blockNumber = 0, node version string =  Parity//v1.11.8-stable-92776e4-20180728/x86_64-linux-gnu/rustc1.27.2
first account of node is 0x000a3702732843418D83A03E65A3d9f7aDd58864, balance is 10000000000 Ether
nodeName: Parity, nodeType: Parity, consensus: ???, network: 8995, chainName: parity-poa-playground, chainId: 8995

Block  0  - waiting for something to happen
(filedate 1535545118) last contract address: 0x536A0b91265dE1Ce1Ba541e54874AC21eC0E63e6
(filedate 1535545811) new contract address: 0x536A0b91265dE1Ce1Ba541e54874AC21eC0E63e6

starting timer, at block 1 which has  1  transactions; at timecode 46494.51728895
block 1 | new #TX  56 / 3000 ms =  18.7 TPS_current | total: #TX   57 /  3.1 s =  18.6 TPS_average
block 2 | new #TX  34 / 5000 ms =   6.8 TPS_current | total: #TX   91 /  7.9 s =  11.5 TPS_average
block 3 | new #TX 513 / 2000 ms = 256.5 TPS_current | total: #TX  604 / 10.1 s =  60.0 TPS_average
block 4 | new #TX 179 / 3000 ms =  59.7 TPS_current | total: #TX  783 / 12.8 s =  61.0 TPS_average
block 5 | new #TX 196 / 3000 ms =  65.3 TPS_current | total: #TX  979 / 15.9 s =  61.6 TPS_average
block 6 | new #TX 189 / 3000 ms =  63.0 TPS_current | total: #TX 1168 / 19.0 s =  61.6 TPS_average
block 7 | new #TX 197 / 3000 ms =  65.7 TPS_current | total: #TX 1365 / 22.0 s =  62.0 TPS_average
block 8 | new #TX 186 / 3000 ms =  62.0 TPS_current | total: #TX 1551 / 25.0 s =  61.9 TPS_average
block 9 | new #TX 194 / 3000 ms =  64.7 TPS_current | total: #TX 1745 / 28.1 s =  62.1 TPS_average
block 10 | new #TX 185 / 3000 ms =  61.7 TPS_current | total: #TX 1930 / 31.1 s =  62.0 TPS_average
block 11 | new #TX 195 / 3000 ms =  65.0 TPS_current | total: #TX 2125 / 33.9 s =  62.7 TPS_average
block 12 | new #TX 187 / 3000 ms =  62.3 TPS_current | total: #TX 2312 / 37.0 s =  62.5 TPS_average
block 13 | new #TX  59 / 2000 ms =  29.5 TPS_current | total: #TX 2371 / 39.1 s =  60.6 TPS_average
...
block 91 | new #TX 645 / 5000 ms = 129.0 TPS_current | total: #TX 18696 / 301.1 s =  62.1 TPS_average
block 92 | new #TX 172 / 3000 ms =  57.3 TPS_current | total: #TX 18868 / 304.1 s =  62.0 TPS_average
block 93 | new #TX  31 / 2000 ms =  15.5 TPS_current | total: #TX 18899 / 306.0 s =  61.8 TPS_average
block 94 | new #TX  81 / 3000 ms =  27.0 TPS_current | total: #TX 18980 / 309.0 s =  61.4 TPS_average
block 95 | new #TX   3 / 3000 ms =   1.0 TPS_current | total: #TX 18983 / 312.1 s =  60.8 TPS_average
block 96 | new #TX 160 / 2000 ms =  80.0 TPS_current | total: #TX 19143 / 314.2 s =  60.9 TPS_average
block 97 | new #TX 163 / 3000 ms =  54.3 TPS_current | total: #TX 19306 / 317.0 s =  60.9 TPS_average
block 98 | new #TX 470 / 2000 ms = 235.0 TPS_current | total: #TX 19776 / 319.1 s =  62.0 TPS_average
block 99 | new #TX 169 / 3000 ms =  56.3 TPS_current | total: #TX 19945 / 321.9 s =  62.0 TPS_average
block 100 | new #TX  56 / 3000 ms =  18.7 TPS_current | total: #TX 20001 / 325.0 s =  61.5 TPS_average
block 101 | new #TX   0 / 110000 ms =   0.0 TPS_current | total: #TX 20001 / 435.2 s =  46.0 TPS_average
block 102 | new #TX   0 / 5000 ms =   0.0 TPS_current | total: #TX 20001 / 440.1 s =  45.4 TPS_average
```

### run4

more  jsonrpc-server-threads

      --jsonrpc-server-threads 20

not better:

```
./tps.py 
...
starting timer, at block 1 which has  1  transactions; at timecode 47560.479835239
block 1 | new #TX 161 / 3000 ms =  53.7 TPS_current | total: #TX  162 /  3.1 s =  53.1 TPS_average
block 2 | new #TX 189 / 3000 ms =  63.0 TPS_current | total: #TX  351 /  6.1 s =  57.6 TPS_average
...
block 107 | new #TX 175 / 3000 ms =  58.3 TPS_current | total: #TX 19960 / 327.2 s =  61.0 TPS_average
block 108 | new #TX  41 / 3000 ms =  13.7 TPS_current | total: #TX 20001 / 330.3 s =  60.6 TPS_average
```

and the CPU was only between 50% and 70%.


### run5
[switching off 4 of the machines](https://github.com/drandreaskrueger/parity-poa-playground/commit/7728566e688b4ab910552d4f302c4621e135f105) (member1, member2, monitor, dashboard), to see whether that accelerates.

```
./tps.py 
...
starting timer, at block 9 which has  1  transactions; at timecode 48112.603595221
block 9 | new #TX 154 / 3000 ms =  51.3 TPS_current | total: #TX  155 /  3.1 s =  50.8 TPS_average
block 10 | new #TX 192 / 3000 ms =  64.0 TPS_current | total: #TX  347 /  6.1 s =  56.9 TPS_average
block 11 | new #TX 198 / 3000 ms =  66.0 TPS_current | total: #TX  545 /  9.1 s =  59.6 TPS_average
...
block 111 | new #TX 195 / 3000 ms =  65.0 TPS_current | total: #TX 19990 / 311.9 s =  64.1 TPS_average
block 112 | new #TX  11 / 3000 ms =   3.7 TPS_current | total: #TX 20001 / 315.0 s =  63.5 TPS_average

```

--> only 2-3 TPS faster.

### run6

With a different network tool, https://github.com/paritytech/parity-deploy/

New that we [had fixed this bug](https://github.com/paritytech/parity-deploy/issues/51#issuecomment-416971456), I could generate a 4 nodes network with the command:

    ./parity-deploy.sh --config aura --name myaura --nodes 4

and then manually edit the resulting `docker-compose.yml`, to remove the buggy line.

And add these parameters to the first `       command: ` line:

    --geth --jsonrpc-server-threads 100 --tx-queue-size 20000 --cache-size 4096 --tracing off --gas-floor-target 100000000000 --pruning fast --tx-queue-mem-limit 0 --no-dapps --no-secretstore-http

And then a 

    docker-compose up

to start the 4 nodes.

Copy the password `paritytech_parity-deploy/deployment/1/password` into `chainhammer/account-passphrase.txt`

Actually, ran the chainhammer now with 1000 multithreading workers:
```
./deploy.py notest; ./send.py threaded2 1000
```

Result log of run 6:

```
./tps.py 
versions: web3 4.3.0, py-solc: 2.1.0, solc 0.4.23+commit.124ca40d.Linux.gpp, testrpc 1.3.4, python 3.5.3 (default, Jan 19 2017, 14:11:04) [GCC 6.3.0 20170118]
web3 connection established, blockNumber = 6, node version string =  Parity//v1.11.8-stable-92776e4-20180728/x86_64-linux-gnu/rustc1.27.2
first account of node is 0xE22e4b61192055b68c65058Ffe1058380dF92769, balance is 0 Ether
nodeName: Parity, nodeType: Parity, consensus: ???, network: 17, chainName: myaura, chainId: 17

Block  6  - waiting for something to happen
(filedate 1535554586) last contract address: 0x977546199b869450d44C6dBCD33652fa36A1e88c
(filedate 1535554624) new contract address: 0x1cEF67D927f0dD94453fCde01dE9c59Eb64A1801

starting timer, at block 7 which has  1  transactions; at timecode 2678.780672846
block 7 | new #TX  56 / 4000 ms =  14.0 TPS_current | total: #TX   57 /  4.3 s =  13.4 TPS_average
block 8 | new #TX 427 / 4000 ms = 106.8 TPS_current | total: #TX  484 /  8.2 s =  59.0 TPS_average
block 9 | new #TX 534 / 8000 ms =  66.8 TPS_current | total: #TX 1018 / 16.1 s =  63.2 TPS_average
block 10 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 1099 / 20.1 s =  54.8 TPS_average
block 11 | new #TX  81 / 2000 ms =  40.5 TPS_current | total: #TX 1180 / 22.2 s =  53.2 TPS_average
block 12 | new #TX 375 / 2000 ms = 187.5 TPS_current | total: #TX 1555 / 24.3 s =  63.9 TPS_average
block 13 | new #TX  66 / 4000 ms =  16.5 TPS_current | total: #TX 1621 / 28.0 s =  58.0 TPS_average
block 14 | new #TX  81 / 2000 ms =  40.5 TPS_current | total: #TX 1702 / 30.1 s =  56.6 TPS_average
block 15 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 1783 / 34.0 s =  52.4 TPS_average
block 16 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 1864 / 38.0 s =  49.1 TPS_average
block 17 | new #TX  48 / 4000 ms =  12.0 TPS_current | total: #TX 1912 / 41.9 s =  45.6 TPS_average
block 18 | new #TX  81 / 2000 ms =  40.5 TPS_current | total: #TX 1993 / 44.1 s =  45.2 TPS_average
block 19 | new #TX 741 / 4000 ms = 185.2 TPS_current | total: #TX 2734 / 48.0 s =  56.9 TPS_average
block 20 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 2815 / 52.3 s =  53.8 TPS_average
block 21 | new #TX 741 / 4000 ms = 185.2 TPS_current | total: #TX 3556 / 56.0 s =  63.5 TPS_average
block 22 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 3637 / 60.3 s =  60.3 TPS_average
block 23 | new #TX 579 / 4000 ms = 144.8 TPS_current | total: #TX 4216 / 64.2 s =  65.6 TPS_average
block 24 | new #TX 529 / 8000 ms =  66.1 TPS_current | total: #TX 4745 / 72.1 s =  65.8 TPS_average
block 25 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 4826 / 76.1 s =  63.4 TPS_average
block 26 | new #TX 466 / 4000 ms = 116.5 TPS_current | total: #TX 5292 / 80.3 s =  65.9 TPS_average
block 27 | new #TX  53 / 4000 ms =  13.2 TPS_current | total: #TX 5345 / 84.3 s =  63.4 TPS_average
block 28 | new #TX 479 / 4000 ms = 119.8 TPS_current | total: #TX 5824 / 88.2 s =  66.0 TPS_average
block 29 | new #TX  44 / 4000 ms =  11.0 TPS_current | total: #TX 5868 / 92.2 s =  63.7 TPS_average
block 30 | new #TX  81 / 2000 ms =  40.5 TPS_current | total: #TX 5949 / 94.3 s =  63.1 TPS_average
block 31 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 6030 / 98.2 s =  61.4 TPS_average
block 32 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 6111 / 102.2 s =  59.8 TPS_average
block 33 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 6192 / 106.1 s =  58.3 TPS_average
block 34 | new #TX 738 / 6000 ms = 123.0 TPS_current | total: #TX 6930 / 112.2 s =  61.8 TPS_average
block 35 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 7011 / 116.1 s =  60.4 TPS_average
block 36 | new #TX  81 / 2000 ms =  40.5 TPS_current | total: #TX 7092 / 118.3 s =  60.0 TPS_average
block 37 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 7173 / 122.2 s =  58.7 TPS_average
block 38 | new #TX  81 / 2000 ms =  40.5 TPS_current | total: #TX 7254 / 124.1 s =  58.5 TPS_average
block 39 | new #TX 736 / 4000 ms = 184.0 TPS_current | total: #TX 7990 / 128.1 s =  62.4 TPS_average
block 40 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 8071 / 132.0 s =  61.1 TPS_average
block 41 | new #TX 736 / 4000 ms = 184.0 TPS_current | total: #TX 8807 / 136.0 s =  64.7 TPS_average
block 42 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 8888 / 140.0 s =  63.5 TPS_average
block 43 | new #TX   7 / 2000 ms =   3.5 TPS_current | total: #TX 8895 / 142.1 s =  62.6 TPS_average
block 44 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 8976 / 146.1 s =  61.4 TPS_average
block 45 | new #TX   2 / 2000 ms =   1.0 TPS_current | total: #TX 8978 / 148.2 s =  60.6 TPS_average
block 46 | new #TX 734 / 4000 ms = 183.5 TPS_current | total: #TX 9712 / 152.2 s =  63.8 TPS_average
block 47 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 9793 / 156.1 s =  62.7 TPS_average
block 48 | new #TX  81 / 6000 ms =  13.5 TPS_current | total: #TX 9874 / 162.2 s =  60.9 TPS_average
block 49 | new #TX  81 / 2000 ms =  40.5 TPS_current | total: #TX 9955 / 164.3 s =  60.6 TPS_average
block 50 | new #TX 733 / 4000 ms = 183.2 TPS_current | total: #TX 10688 / 168.0 s =  63.6 TPS_average
block 51 | new #TX 733 / 8000 ms =  91.6 TPS_current | total: #TX 11421 / 176.2 s =  64.8 TPS_average
block 52 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 11502 / 180.2 s =  63.8 TPS_average
block 53 | new #TX  81 / 2000 ms =  40.5 TPS_current | total: #TX 11583 / 182.0 s =  63.6 TPS_average
block 54 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 11664 / 186.0 s =  62.7 TPS_average
block 55 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 11745 / 190.2 s =  61.7 TPS_average
block 56 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 11826 / 194.1 s =  60.9 TPS_average
block 57 | new #TX  81 / 2000 ms =  40.5 TPS_current | total: #TX 11907 / 196.3 s =  60.7 TPS_average
block 58 | new #TX 730 / 4000 ms = 182.5 TPS_current | total: #TX 12637 / 200.2 s =  63.1 TPS_average
block 59 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 12718 / 204.2 s =  62.3 TPS_average
block 60 | new #TX 730 / 4000 ms = 182.5 TPS_current | total: #TX 13448 / 208.1 s =  64.6 TPS_average
block 61 | new #TX 730 / 8000 ms =  91.2 TPS_current | total: #TX 14178 / 216.1 s =  65.6 TPS_average
block 62 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 14259 / 220.0 s =  64.8 TPS_average
block 63 | new #TX 620 / 4000 ms = 155.0 TPS_current | total: #TX 14879 / 224.3 s =  66.3 TPS_average
block 64 | new #TX  74 / 4000 ms =  18.5 TPS_current | total: #TX 14953 / 227.9 s =  65.6 TPS_average
block 65 | new #TX   9 / 2000 ms =   4.5 TPS_current | total: #TX 14962 / 230.1 s =  65.0 TPS_average
block 66 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 15043 / 234.0 s =  64.3 TPS_average
block 67 | new #TX  81 / 2000 ms =  40.5 TPS_current | total: #TX 15124 / 236.1 s =  64.0 TPS_average
block 68 | new #TX 728 / 4000 ms = 182.0 TPS_current | total: #TX 15852 / 240.1 s =  66.0 TPS_average
block 69 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 15933 / 244.1 s =  65.3 TPS_average
block 70 | new #TX 504 / 4000 ms = 126.0 TPS_current | total: #TX 16437 / 248.0 s =  66.3 TPS_average
block 71 | new #TX  30 / 4000 ms =   7.5 TPS_current | total: #TX 16467 / 252.3 s =  65.3 TPS_average
block 72 | new #TX 482 / 4000 ms = 120.5 TPS_current | total: #TX 16949 / 256.0 s =  66.2 TPS_average
block 73 | new #TX  12 / 4000 ms =   3.0 TPS_current | total: #TX 16961 / 260.2 s =  65.2 TPS_average
block 74 | new #TX 519 / 4000 ms = 129.8 TPS_current | total: #TX 17480 / 264.2 s =  66.2 TPS_average
block 75 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 17561 / 268.1 s =  65.5 TPS_average
block 76 | new #TX 444 / 4000 ms = 111.0 TPS_current | total: #TX 18005 / 272.1 s =  66.2 TPS_average
block 77 | new #TX  68 / 4000 ms =  17.0 TPS_current | total: #TX 18073 / 276.1 s =  65.5 TPS_average
block 78 | new #TX 448 / 4000 ms = 112.0 TPS_current | total: #TX 18521 / 280.1 s =  66.1 TPS_average
block 79 | new #TX  51 / 4000 ms =  12.8 TPS_current | total: #TX 18572 / 284.1 s =  65.4 TPS_average
block 80 | new #TX 459 / 4000 ms = 114.8 TPS_current | total: #TX 19031 / 288.0 s =  66.1 TPS_average
block 81 | new #TX  46 / 4000 ms =  11.5 TPS_current | total: #TX 19077 / 292.3 s =  65.3 TPS_average
block 82 | new #TX 460 / 4000 ms = 115.0 TPS_current | total: #TX 19537 / 296.0 s =  66.0 TPS_average
block 83 | new #TX  30 / 4000 ms =   7.5 TPS_current | total: #TX 19567 / 300.2 s =  65.2 TPS_average
block 84 | new #TX  81 / 2000 ms =  40.5 TPS_current | total: #TX 19648 / 302.1 s =  65.0 TPS_average
block 85 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 19729 / 306.1 s =  64.5 TPS_average
block 86 | new #TX  81 / 4000 ms =  20.2 TPS_current | total: #TX 19810 / 310.1 s =  63.9 TPS_average
block 87 | new #TX 191 / 2000 ms =  95.5 TPS_current | total: #TX 20001 / 312.3 s =  64.1 TPS_average
block 88 | new #TX   0 / 114000 ms =   0.0 TPS_current | total: #TX 20001 / 426.2 s =  46.9 TPS_average
```

again, **--> only 2-3 TPS faster.**


### run7

With inspiration from @ddorgan, see [issue#9393](https://github.com/paritytech/parity-ethereum/issues/9393#issuecomment-416995893):

> --gas-floor-target of something more realistic would be a good idea ... e.g. maybe 20m ...   

explanation:

> --gas-floor-target Amount of gas per block to target when sealing a new block (default: 4700000).  
> https://hudsonjameson.com/2017-06-27-accounts-transactions-gas-ethereum/  

New run with 40,000,000 gas-floor-target: 

First, add all our parameters to [the 5 template files, see this feature request](https://github.com/paritytech/parity-deploy/issues/55#issuecomment-418290906), then delete whatever was there:

```
docker-compose down -v
sudo rm -rf data/ deployment/ docker-compose.yml
```
and make a new deployment:
```
./parity-deploy.sh --config aura --name myaura --nodes 4 
cat deployment/1/password
docker-compose up
```

the password goes into `chainhammer/account-passphrase.txt`.

(Just as a test) **single threaded**, i.e. calling the chainhammer with:

```
 ./deploy.py notest; ./send.py
```
we see more than 50 TPS:

```
./tps.py 
[...]

starting timer, at block 1 which has  1  transactions; at timecode 7680.982321106
block 1 | new #TX  24 / 2000 ms =  12.0 TPS_current | total: #TX   25 /  2.1 s =  11.7 TPS_average
block 2 | new #TX 101 / 4000 ms =  25.2 TPS_current | total: #TX  126 /  6.1 s =  20.7 TPS_average
block 3 | new #TX 200 / 4000 ms =  50.0 TPS_current | total: #TX  326 / 10.0 s =  32.5 TPS_average
[...]
block 81 | new #TX 200 / 6000 ms =  33.3 TPS_current | total: #TX 16649 / 317.9 s =  52.4 TPS_average
block 82 | new #TX  39 / 4000 ms =   9.8 TPS_current | total: #TX 16688 / 321.9 s =  51.8 TPS_average
block 83 | new #TX 429 / 2000 ms = 214.5 TPS_current | total: #TX 17117 / 324.0 s =  52.8 TPS_average
block 84 | new #TX 151 / 4000 ms =  37.8 TPS_current | total: #TX 17268 / 327.9 s =  52.7 TPS_average
block 85 | new #TX  98 / 2000 ms =  49.0 TPS_current | total: #TX 17366 / 330.1 s =  52.6 TPS_average
block 86 | new #TX 200 / 4000 ms =  50.0 TPS_current | total: #TX 17566 / 334.0 s =  52.6 TPS_average
block 87 | new #TX   5 / 2000 ms =   2.5 TPS_current | total: #TX 17571 / 336.2 s =  52.3 TPS_average
block 88 | new #TX 314 / 4000 ms =  78.5 TPS_current | total: #TX 17885 / 340.1 s =  52.6 TPS_average
block 89 | new #TX 137 / 4000 ms =  34.2 TPS_current | total: #TX 18022 / 344.1 s =  52.4 TPS_average
block 90 | new #TX 125 / 2000 ms =  62.5 TPS_current | total: #TX 18147 / 346.2 s =  52.4 TPS_average
block 91 | new #TX 188 / 4000 ms =  47.0 TPS_current | total: #TX 18335 / 350.1 s =  52.4 TPS_average
block 92 | new #TX 187 / 4000 ms =  46.8 TPS_current | total: #TX 18522 / 354.1 s =  52.3 TPS_average
block 93 | new #TX 187 / 4000 ms =  46.8 TPS_current | total: #TX 18709 / 358.0 s =  52.3 TPS_average
block 94 | new #TX 167 / 4000 ms =  41.8 TPS_current | total: #TX 18876 / 362.0 s =  52.1 TPS_average
block 95 | new #TX 200 / 4000 ms =  50.0 TPS_current | total: #TX 19076 / 365.9 s =  52.1 TPS_average
block 96 | new #TX 200 / 4000 ms =  50.0 TPS_current | total: #TX 19276 / 370.2 s =  52.1 TPS_average
block 97 | new #TX  16 / 4000 ms =   4.0 TPS_current | total: #TX 19292 / 373.8 s =  51.6 TPS_average
block 98 | new #TX 187 / 2000 ms =  93.5 TPS_current | total: #TX 19479 / 376.0 s =  51.8 TPS_average
block 99 | new #TX 323 / 4000 ms =  80.8 TPS_current | total: #TX 19802 / 380.0 s =  52.1 TPS_average
block 100 | new #TX 138 / 4000 ms =  34.5 TPS_current | total: #TX 19940 / 383.9 s =  51.9 TPS_average
block 101 | new #TX  61 / 4000 ms =  15.2 TPS_current | total: #TX 20001 / 387.9 s =  51.6 TPS_average
```

and **multithreaded with e.g. 10 workers**: 
```
./deploy.py notest; ./send.py threaded2 10
```
we can push that (only) about 20% higher:

```
./tps.py 
versions: web3 4.3.0, py-solc: 2.1.0, solc 0.4.23+commit.124ca40d.Linux.gpp, testrpc 1.3.4, python 3.5.3 (default, Jan 19 2017, 14:11:04) [GCC 6.3.0 20170118]
web3 connection established, blockNumber = 2, node version string =  Parity//v1.11.8-stable-92776e4-20180728/x86_64-linux-gnu/rustc1.27.2
first account of node is 0x50fa19134E0789E9257dF8A3E9c3dEb66053F0c6, balance is 0 Ether
nodeName: Parity, nodeType: Parity, consensus: ???, network: 17, chainName: myaura, chainId: 17

Block  2  - waiting for something to happen
(filedate 1536057340) last contract address: 0x85f8A6629eA4C68Ea3BF106D3Ca135Edf96D4aD9
(filedate 1536057366) new contract address: 0x135fA586EC1aBe436A7a4677899947d3de522a35

starting timer, at block 3 which has  1  transactions; at timecode 10002.910648046
block 3 | new #TX  37 / 4000 ms =   9.2 TPS_current | total: #TX   38 /  3.9 s =   9.6 TPS_average
block 4 | new #TX   2 / 2000 ms =   1.0 TPS_current | total: #TX   40 /  6.1 s =   6.6 TPS_average
block 5 | new #TX 198 / 2000 ms =  99.0 TPS_current | total: #TX  238 /  8.2 s =  29.0 TPS_average
block 6 | new #TX 200 / 4000 ms =  50.0 TPS_current | total: #TX  438 / 12.1 s =  36.1 TPS_average
block 7 | new #TX 200 / 2000 ms = 100.0 TPS_current | total: #TX  638 / 14.3 s =  44.7 TPS_average
block 8 | new #TX 513 / 4000 ms = 128.2 TPS_current | total: #TX 1151 / 18.2 s =  63.1 TPS_average
block 9 | new #TX  61 / 4000 ms =  15.2 TPS_current | total: #TX 1212 / 21.9 s =  55.3 TPS_average
block 10 | new #TX 466 / 4000 ms = 116.5 TPS_current | total: #TX 1678 / 26.2 s =  64.2 TPS_average
block 11 | new #TX  40 / 4000 ms =  10.0 TPS_current | total: #TX 1718 / 30.1 s =  57.1 TPS_average
block 12 | new #TX 200 / 6000 ms =  33.3 TPS_current | total: #TX 1918 / 36.2 s =  53.0 TPS_average
block 13 | new #TX 200 / 2000 ms = 100.0 TPS_current | total: #TX 2118 / 38.0 s =  55.7 TPS_average
block 14 | new #TX 607 / 4000 ms = 151.8 TPS_current | total: #TX 2725 / 42.0 s =  64.9 TPS_average
block 15 | new #TX  22 / 4000 ms =   5.5 TPS_current | total: #TX 2747 / 45.9 s =  59.8 TPS_average
block 16 | new #TX 200 / 2000 ms = 100.0 TPS_current | total: #TX 2947 / 48.1 s =  61.3 TPS_average
block 17 | new #TX 200 / 4000 ms =  50.0 TPS_current | total: #TX 3147 / 52.3 s =  60.1 TPS_average
block 18 | new #TX 200 / 4000 ms =  50.0 TPS_current | total: #TX 3347 / 56.0 s =  59.8 TPS_average
block 19 | new #TX 200 / 4000 ms =  50.0 TPS_current | total: #TX 3547 / 60.2 s =  58.9 TPS_average
block 20 | new #TX 200 / 4000 ms =  50.0 TPS_current | total: #TX 3747 / 64.2 s =  58.4 TPS_average
block 21 | new #TX 557 / 2000 ms = 278.5 TPS_current | total: #TX 4304 / 66.0 s =  65.2 TPS_average
block 22 | new #TX  63 / 4000 ms =  15.8 TPS_current | total: #TX 4367 / 70.0 s =  62.4 TPS_average
block 23 | new #TX 460 / 4000 ms = 115.0 TPS_current | total: #TX 4827 / 74.2 s =  65.0 TPS_average
block 24 | new #TX  60 / 4000 ms =  15.0 TPS_current | total: #TX 4887 / 77.9 s =  62.7 TPS_average
block 25 | new #TX 200 / 2000 ms = 100.0 TPS_current | total: #TX 5087 / 80.0 s =  63.6 TPS_average
block 26 | new #TX 200 / 8000 ms =  25.0 TPS_current | total: #TX 5287 / 87.9 s =  60.1 TPS_average
block 27 | new #TX   6 / 4000 ms =   1.5 TPS_current | total: #TX 5293 / 92.2 s =  57.4 TPS_average
block 28 | new #TX 200 / 4000 ms =  50.0 TPS_current | total: #TX 5493 / 96.1 s =  57.2 TPS_average
block 29 | new #TX  27 / 4000 ms =   6.8 TPS_current | total: #TX 5520 / 100.1 s =  55.2 TPS_average
block 30 | new #TX 200 / 2000 ms = 100.0 TPS_current | total: #TX 5720 / 102.2 s =  56.0 TPS_average
block 31 | new #TX 1194 / 4000 ms = 298.5 TPS_current | total: #TX 6914 / 106.2 s =  65.1 TPS_average
block 32 | new #TX 532 / 8000 ms =  66.5 TPS_current | total: #TX 7446 / 114.1 s =  65.2 TPS_average
block 33 | new #TX  66 / 4000 ms =  16.5 TPS_current | total: #TX 7512 / 118.1 s =  63.6 TPS_average
block 34 | new #TX 200 / 6000 ms =  33.3 TPS_current | total: #TX 7712 / 124.2 s =  62.1 TPS_average
block 35 | new #TX   3 / 4000 ms =   0.8 TPS_current | total: #TX 7715 / 128.2 s =  60.2 TPS_average
block 36 | new #TX 770 / 2000 ms = 385.0 TPS_current | total: #TX 8485 / 130.3 s =  65.1 TPS_average
block 37 | new #TX  43 / 4000 ms =  10.8 TPS_current | total: #TX 8528 / 134.0 s =  63.7 TPS_average
block 38 | new #TX 470 / 4000 ms = 117.5 TPS_current | total: #TX 8998 / 137.9 s =  65.2 TPS_average
block 39 | new #TX  36 / 4000 ms =   9.0 TPS_current | total: #TX 9034 / 142.2 s =  63.5 TPS_average
block 40 | new #TX 489 / 4000 ms = 122.2 TPS_current | total: #TX 9523 / 146.1 s =  65.2 TPS_average
block 41 | new #TX  26 / 4000 ms =   6.5 TPS_current | total: #TX 9549 / 150.1 s =  63.6 TPS_average
block 42 | new #TX 200 / 6000 ms =  33.3 TPS_current | total: #TX 9749 / 156.2 s =  62.4 TPS_average
block 43 | new #TX 200 / 2000 ms = 100.0 TPS_current | total: #TX 9949 / 158.0 s =  63.0 TPS_average
block 44 | new #TX 605 / 4000 ms = 151.2 TPS_current | total: #TX 10554 / 162.0 s =  65.2 TPS_average
block 45 | new #TX 522 / 8000 ms =  65.2 TPS_current | total: #TX 11076 / 169.9 s =  65.2 TPS_average
block 46 | new #TX  84 / 4000 ms =  21.0 TPS_current | total: #TX 11160 / 174.2 s =  64.1 TPS_average
block 47 | new #TX 449 / 4000 ms = 112.2 TPS_current | total: #TX 11609 / 178.2 s =  65.2 TPS_average
block 48 | new #TX  61 / 4000 ms =  15.2 TPS_current | total: #TX 11670 / 182.1 s =  64.1 TPS_average
block 49 | new #TX 462 / 4000 ms = 115.5 TPS_current | total: #TX 12132 / 186.1 s =  65.2 TPS_average
block 50 | new #TX  47 / 4000 ms =  11.8 TPS_current | total: #TX 12179 / 190.0 s =  64.1 TPS_average
block 51 | new #TX 468 / 4000 ms = 117.0 TPS_current | total: #TX 12647 / 194.0 s =  65.2 TPS_average
block 52 | new #TX  48 / 4000 ms =  12.0 TPS_current | total: #TX 12695 / 197.9 s =  64.1 TPS_average
block 53 | new #TX 108 / 2000 ms =  54.0 TPS_current | total: #TX 12803 / 200.0 s =  64.0 TPS_average
block 54 | new #TX 374 / 2000 ms = 187.0 TPS_current | total: #TX 13177 / 202.2 s =  65.2 TPS_average
block 55 | new #TX  57 / 4000 ms =  14.2 TPS_current | total: #TX 13234 / 206.1 s =  64.2 TPS_average
block 56 | new #TX 457 / 4000 ms = 114.2 TPS_current | total: #TX 13691 / 210.1 s =  65.2 TPS_average
block 57 | new #TX   9 / 4000 ms =   2.2 TPS_current | total: #TX 13700 / 214.0 s =  64.0 TPS_average
block 58 | new #TX 516 / 4000 ms = 129.0 TPS_current | total: #TX 14216 / 218.1 s =  65.2 TPS_average
block 59 | new #TX  68 / 4000 ms =  17.0 TPS_current | total: #TX 14284 / 222.1 s =  64.3 TPS_average
block 60 | new #TX 447 / 4000 ms = 111.8 TPS_current | total: #TX 14731 / 226.1 s =  65.2 TPS_average
block 61 | new #TX  65 / 4000 ms =  16.2 TPS_current | total: #TX 14796 / 230.0 s =  64.3 TPS_average
block 62 | new #TX 200 / 6000 ms =  33.3 TPS_current | total: #TX 14996 / 236.1 s =  63.5 TPS_average
block 63 | new #TX 200 / 4000 ms =  50.0 TPS_current | total: #TX 15196 / 240.0 s =  63.3 TPS_average
block 64 | new #TX   5 / 4000 ms =   1.2 TPS_current | total: #TX 15201 / 244.0 s =  62.3 TPS_average
block 65 | new #TX 195 / 2000 ms =  97.5 TPS_current | total: #TX 15396 / 246.1 s =  62.6 TPS_average
block 66 | new #TX 897 / 4000 ms = 224.2 TPS_current | total: #TX 16293 / 250.1 s =  65.2 TPS_average
block 67 | new #TX  30 / 4000 ms =   7.5 TPS_current | total: #TX 16323 / 254.0 s =  64.3 TPS_average
block 68 | new #TX 503 / 4000 ms = 125.8 TPS_current | total: #TX 16826 / 258.0 s =  65.2 TPS_average
block 69 | new #TX  23 / 4000 ms =   5.8 TPS_current | total: #TX 16849 / 261.9 s =  64.3 TPS_average
block 70 | new #TX 200 / 2000 ms = 100.0 TPS_current | total: #TX 17049 / 264.1 s =  64.6 TPS_average
block 71 | new #TX 307 / 2000 ms = 153.5 TPS_current | total: #TX 17356 / 266.2 s =  65.2 TPS_average
block 72 | new #TX  20 / 4000 ms =   5.0 TPS_current | total: #TX 17376 / 270.1 s =  64.3 TPS_average
block 73 | new #TX 514 / 4000 ms = 128.5 TPS_current | total: #TX 17890 / 274.1 s =  65.3 TPS_average
block 74 | new #TX  74 / 4000 ms =  18.5 TPS_current | total: #TX 17964 / 278.1 s =  64.6 TPS_average
block 75 | new #TX 200 / 2000 ms = 100.0 TPS_current | total: #TX 18164 / 280.2 s =  64.8 TPS_average
block 76 | new #TX 152 / 4000 ms =  38.0 TPS_current | total: #TX 18316 / 284.2 s =  64.5 TPS_average
block 77 | new #TX 200 / 4000 ms =  50.0 TPS_current | total: #TX 18516 / 288.1 s =  64.3 TPS_average
block 78 | new #TX 426 / 2000 ms = 213.0 TPS_current | total: #TX 18942 / 290.2 s =  65.3 TPS_average
block 79 | new #TX  66 / 4000 ms =  16.5 TPS_current | total: #TX 19008 / 294.2 s =  64.6 TPS_average
block 80 | new #TX 454 / 4000 ms = 113.5 TPS_current | total: #TX 19462 / 298.1 s =  65.3 TPS_average
block 81 | new #TX  54 / 4000 ms =  13.5 TPS_current | total: #TX 19516 / 302.1 s =  64.6 TPS_average
block 82 | new #TX 481 / 4000 ms = 120.2 TPS_current | total: #TX 19997 / 306.0 s =  65.3 TPS_average
block 83 | new #TX   4 / 4000 ms =   1.0 TPS_current | total: #TX 20001 / 310.1 s =  64.5 TPS_average
```

#### result run 7

![https://gitlab.com/electronDLT/chainhammer/raw/master/chainreader/img/parity-aura_run7_tps-bt-bs-gas_blks3-90.png](https://gitlab.com/electronDLT/chainhammer/raw/master/chainreader/img/parity-aura_run7_tps-bt-bs-gas_blks3-90.png)
diagram https://gitlab.com/electronDLT/chainhammer/blob/master/chainreader/img/parity-aura_run7_tps-bt-bs-gas_blks3-90.png

N.B.: The CPU usage stays below 60%, so parity is not yet using all the computational resources available, even with `--jsonrpc-server-threads 100`. 


**We need new ideas how to accelerate parity !!**

## Please you help

Compared to e.g. the >400 TPS of [quorum-IBFT](quorum-IBFT.md#result-400-tps-but-only-for-the-first-14k-tx), and the >300 TPS of [geth-Clique](https://gitlab.com/electronDLT/chainhammer/blob/master/geth.md#results-approx-350-tps-but-only-for-first-14k-transactions), this is slow. 

Calling all parity experts: How to improve this? See issue [PE#9393](https://github.com/paritytech/parity-ethereum/issues/9393). Thanks.

### There is a [README.md --> quickstart](README.md#quickstart) now ... 
... so if you have any intution or knowledge how to accelerate this, please replicate my setup, and then start modifying the parameters of the network of parity nodes, with e.g. `parity-deploy.sh` - until you get to better TPS rates. 

Then please alert us how you did it. Thanks.



## issues
* [PD#51](https://github.com/paritytech/parity-deploy/issues/51) libstdc++.so.6: version `GLIBCXX_3.4.22' not found
* [PE#9390](https://github.com/paritytech/parity-ethereum/issues/9390) (dockerized parity) libstdc++.so.6: version `GLIBCXX_3.4.22' not found
* [PD#52](https://github.com/paritytech/parity-deploy/issues/52) Invalid node address format given for a boot node
* [PPP#14](https://github.com/orbita-center/parity-poa-playground/issues/14) block interval?
* [PPP#15](https://github.com/orbita-center/parity-poa-playground/issues/15) (FR) script which only deletes the blockchains from all nodes
* [PE#9393](https://github.com/paritytech/parity-ethereum/issues/9393) 60 TPS ? (parity aura v1.11.8)
* [PE#9432](https://github.com/paritytech/parity-ethereum/issues/9432) (FR) new standardized RPC query with standardized answer
* [PPP#17](https://github.com/orbita-center/parity-poa-playground/issues/17) warnings and errors
* [PD#55](https://github.com/paritytech/parity-deploy/issues/55) (FR) user defined parameters

