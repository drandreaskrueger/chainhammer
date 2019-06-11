# Chainhammer Polkadot instructions

## polkadot-deployer
### cloud
The below `polkadot-deployer` shows strange problems on my local Debian machine, so eventually I decided to develop on a cloud machine instead:

AWS, based on image "debian-stretch-hvm-x86_64-gp2-2019-05-14-84483" (for identical replication of the problems mentioned below **please use the exact same AMI "ami-0faa9c9b5399088fd"**); then install nodejs, npm, docker:

```
curl -sL https://deb.nodesource.com/setup_10.x | sudo bash -
sudo apt-get install gcc g++ make nodejs git
curl -L https://npmjs.org/install.sh | sudo sh

git clone https://github.com/drandreaskrueger/chainhammer
chainhammer/scripts/install-docker.sh 
exit
```
logout and log back in, so that $USER is in docker group:
```
groups; docker --version
  admin adm [...] docker
  Docker version 18.09.6, build 481bc77
```

I had EACCES access rights problems (and for all 4 ways of npm install: `npm i $PRG`, `npm i -g $PRG`, `sudo npm i $PRG`, `sudo npm i -g $PRG`), until I used this:
```
mkdir ~/.npm-global
sudo chown -R $USER ~/.npm-global
npm config set prefix '~/.npm-global'

nano ~/.profile
    export PATH=~/.npm-global/bin:$PATH
source ~/.profile
```

better use swap as RAM might become scarce
```
SWAPFILE=/swapfile && free -m && sudo swapoff -a && sudo dd if=/dev/zero of=$SWAPFILE bs=1M count=2000 && sudo chmod 600 $SWAPFILE && sudo mkswap $SWAPFILE && echo $SWAPFILE none swap defaults 0 0 | sudo tee -a /etc/fstab && sudo swapon -a && free -m
```

situation:
```
node --version; npm --version; docker --version; free -m; df -h
```
> node v10.16.0  
> npm 6.9.0  
> Docker version 18.09.6, build 481bc77  

>   total        used        free      shared  buff/cache   available  
> Mem:           2002          95          79           5        1827        1718  
> Swap:          1999           0        1999  
>  
> Filesystem      Size  Used Avail Use% Mounted on  
> /dev/xvda1      7.9G  4.1G  3.4G  55% /  




### polkadot-deployer install and run
```
npm i -g polkadot-deployer
polkadot-deployer --version
```
> 0.9.2  

```
polkadot-deployer --help
polkadot-deployer list

docker system prune -a --volumes
docker system prune -a --volumes # yes, twice
polkadot-deployer create --verbose --config testnet1.json
```
with `testnet1.json`:
```
{
  "name": "testnet1",
  "type": "local",
  "nodes": 4
}
```

#### troubleshooting with kubectl
install kubectl (here Debian/ubuntu, but [see this](https://kubernetes.io/docs/tasks/tools/install-kubectl/) for other systems):
```
sudo apt-get update && sudo apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubectl
kubectl version
```
> Client Version: version.Info{Major:"1", Minor:"14", GitVersion:"v1.14.3", GitCommit:"5e53fd6bc17c0dec8434817e69b04a25d8ae0ff0", GitTreeState:"clean", BuildDate:"2019-06-06T01:44:30Z", GoVersion:"go1.12.5", Compiler:"gc", Platform:"linux/amd64"}

then get the config file from `localhost:10080` and show it via `kubectl`
```
wget -O config http://localhost:10080/config
kubectl --kubeconfig=./config describe node minikube
```
at the moment [polkadot-deployer still does not start up properly](https://github.com/w3f/polkadot-deployer/issues/5#issuecomment-499876296); seemingly because [bsycorp/kind-v1.13 causes problems in approx 1 out of 3 attemps to start it](https://github.com/bsycorp/kind/issues/22). Waiting until they come up with a solution ...


## issues
* [wpd#5](https://github.com/w3f/polkadot-deployer/issues/5) log files?
* [bk#22](https://github.com/bsycorp/kind/issues/22) bsycorp/kind works only when started twice
