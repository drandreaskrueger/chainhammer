# chainhammer
Actually, today I tried this again - tested on and optimized for Debian AWS machine (`debian-stretch-hvm-x86_64-gp2-2018-08-20-85640`) - all this really does work:
## How to replicate the results

### toolchain
```
# docker
# this is for Debian Linux, 
# if you run a different distro, google "install docker [distro name]"
sudo apt-get update 
sudo apt-get -y remove docker docker-engine docker.io 
sudo apt-get install -y apt-transport-https ca-certificates wget software-properties-common
wget https://download.docker.com/linux/debian/gpg 
sudo apt-key add gpg
rm gpg
echo "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee -a /etc/apt/sources.list.d/docker.list
sudo apt-get update
sudo apt-cache policy docker-ce
sudo apt-get -y install docker-ce 
sudo systemctl start docker

sudo usermod -aG docker ${USER}
groups $USER
```
log out and log back in, to enable those usergroup changes

```
# docker compose new version
sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod 755 /usr/local/bin/docker-compose
docker-compose --version
```
> docker-compose version 1.22.0, build f46880fe



```
# parity-deploy
# for a dockerized parity environment
# this is instantseal, NOT a realistic network of nodes
# for 8 different setups see chainhammer-->parity.md
git clone https://github.com/paritytech/parity-deploy.git paritytech_parity-deploy
cd paritytech_parity-deploy
sudo ./clean.sh
./parity-deploy.sh --config dev --name instantseal --geth
docker-compose up
```

new terminal:
```
# solc
# someone should PLEASE create a Debian specific installation routine
# see https://solidity.readthedocs.io/en/latest/installing-solidity.html 
# and https://github.com/ethereum/solidity/releases
wget https://github.com/ethereum/solidity/releases/download/v0.4.24/solc-static-linux
chmod 755 solc-static-linux 
echo $PATH
sudo mv solc-static-linux /usr/local/bin/
sudo ln -s /usr/local/bin/solc-static-linux /usr/local/bin/solc
solc --version
```

> Version: 0.4.24+commit.e67f0147.Linux.g++

### chainhammer
```
# chainhammer & dependencies
git clone https://gitlab.com/electronDLT/chainhammer electronDLT_chainhammer
cd electronDLT_chainhammer/

sudo apt install python3-pip libssl-dev
sudo pip3 install virtualenv 
virtualenv -p python3 py3eth
source py3eth/bin/activate

python3 -m pip install --upgrade pip==18.0
pip3 install --upgrade py-solc==2.1.0 web3==4.3.0 web3[tester]==4.3.0 rlp==0.6.0 eth-testrpc==1.3.4 requests pandas jupyter ipykernel matplotlib
ipython kernel install --user --name="Python.3.py3eth"
```

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
cd electronDLT_chainhammer/
source py3eth/bin/activate

# start the chainhammer send routine
./deploy.py notest; ./send.py 
```

or:

```
# not blocking but with 23 multi-threading workers
./deploy.py notest; ./send.py threaded2 23
```

### everything below here is *not* necessary

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

### geth

( * ) I do *not* want to install `geth` locally, but start the geth console *from a docker container* - but I don't succeed:

```
docker run ethereum/client-go attach https://localhost:8545
```
> WARN [09-10|09:38:24.984] Sanitizing cache to Go's GC limits       provided=1024 updated=331  
> Fatal: Failed to start the JavaScript console: api modules: Post https://localhost:8545: dial tcp 127.0.0.1:8545: connect: connection refused  
> Fatal: Failed to start the JavaScript console: api modules: Post https://localhost:8545: dial tcp 127.0.0.1:8545: connect: connection refused  

Please help me with ^ this, thanks.

---

Until that is sorted, I simply install `geth` locally:

```
wget https://dl.google.com/go/go1.11.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.11.linux-amd64.tar.gz 
rm go1.11.linux-amd64.tar.gz 
echo "export PATH=\$PATH:/usr/local/go/bin:~/go/bin" >> .profile
```
logout, log back in
```
go version
```
> go version go1.11 linux/amd64

```
go get -d github.com/ethereum/go-ethereum
go install github.com/ethereum/go-ethereum/cmd/geth
geth version
```
> geth version  
> WARN [09-10|09:56:11.759] Sanitizing cache to Go's GC limits       provided=1024 updated=331  
> Geth  
> Version: 1.8.16-unstable  
> Architecture: amd64  
> Protocol Versions: [63 62]  
> Network Id: 1  
> Go Version: go1.11  
> Operating System: linux  
> GOPATH=  
> GOROOT=/usr/local/go  


### please you now try this

And about "not having the time" - these 2.5 hours happened on my FREE DAY. I must convince them now that I can take those hours off again.

### quorum IBFT
now compare the poor TPS performance of `parity aura` with `quorum/geth IBFT`:

#### stop parity
Kill the above `parity-deploy.sh ...; docker-compose up` with:

Ctrl-C, then

```
docker-compose down -v
```
you might run out of disk space, so better delete all other docker stuff:
```
docker kill $(docker ps -q) ; docker rm $(docker ps -a -q) ; docker rmi $(docker images -q)
```

#### quorum IBFT network with 4 dockerized nodes
for details see [quorum-IBFT.md#crux-docker-4nodes](https://gitlab.com/electronDLT/chainhammer/blob/db3ae5da577d9b9d44c2879434993f3e0d44899f/quorum-IBFT.md#crux-docker-4nodes).

```
git clone https://github.com/drandreaskrueger/crux.git drandreaskrueger_crux
cd drandreaskrueger_crux

cd docker/quorum-crux/
docker-compose -f docker-compose-local.yaml up --build
```
wait until you see

```
...
```

(I am pausing this, [until blk-io have fixed their issue](https://github.com/blk-io/crux/issues/37). Then: )

new terminal
```
cd electronDLT_chainhammer/
source py3eth/bin/activate

./tps.py
```

new terminal
```
cd electronDLT_chainhammer/
source py3eth/bin/activate

./deploy.py notest; ./send.py 
```



## AWS deployment

This first part here you can safely ignore, it just logs what I have done to create the AMI:

### how I created the AMI
* [Launch instance Wizard](https://eu-west-2.console.aws.amazon.com/ec2/v2/home?region=eu-west-2#LaunchInstanceWizard:) in  `eu-west-2` (London)
* Community AMIs, search "Debian-stretch 2018"
* newest is `debian-stretch-hvm-x86_64-gp2-2018-08-20-85640`
  * ami-0e5de816bb166040f
  * FAI Debian image
  * Root device type: ebs 
  * Virtualization type: hvm`
* type `t2.micro`
* Step 3: Configure Instance Details
  * Network: Default
  * Subnet: Default in eu-west-2a
  * auto assign public IP
* Step 5: Add Tags
  * Name: chainhammer
  * Environment: dev
  * Project: benchmarking
  * Owner: Andreas Krueger
* create new security group, name it; allow ssh access
* choose an existing ssh keypair `AndreasKeypairAWS.pem`

simplify ssh access, by adding this block to

```
nano ~/.ssh/config
```

```
Host chainhammer
  Hostname ec2-18-130-226-69.eu-west-2.compute.amazonaws.com
  StrictHostKeyChecking no
  User admin
  IdentityFile ~/.ssh/AndreasKeypairAWS.pem
```
now it's this simple to connect:
```
ssh chainhammer
```
Then I executed all the above instructions, to install the toolchain, and chainhammer.

### how you can use my AMI to quickstart your benchmarking

TODO