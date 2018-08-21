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




## issues
* [PD#51](https://github.com/paritytech/parity-deploy/issues/51) libstdc++.so.6: version `GLIBCXX_3.4.22' not found
* [PE#9390](https://github.com/paritytech/parity-ethereum/issues/9390) (dockerized parity) libstdc++.so.6: version `GLIBCXX_3.4.22' not found
* [PD#52](https://github.com/paritytech/parity-deploy/issues/52) Invalid node address format given for a boot node