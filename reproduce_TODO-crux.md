

#### quorum IBFT network with 4 dockerized nodes
for details see [quorum-IBFT.md#crux-docker-4nodes](https://gitlab.com/electronDLT/chainhammer/blob/db3ae5da577d9b9d44c2879434993f3e0d44899f/quorum-IBFT.md#crux-docker-4nodes).

```
git clone https://github.com/drandreaskrueger/crux.git drandreaskrueger_crux
cd drandreaskrueger_crux

cd docker/quorum-crux/
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

##### problem
something isn't working yet. Cannot connect to node, when installed on AWS:

```
geth attach http://localhost:22001
Fatal: Failed to start the JavaScript console: api modules: Post http://localhost:22001: EOF
```

no time for that now. 

not using quorum-crux for now; instead use plain vanilla `geth`.
