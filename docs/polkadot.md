# Chainhammer Polkadot instructions

## polkadot-deployer
### node & npm - upgrade and versions:
```
sudo npm cache clean -f
sudo npm install -g n
sudo n stable
sudo npm install -g npm
node --version; npm --version; docker --version
```
> node v10.16.0  
> npm 6.9.0  
> Docker version 18.09.6, build 481bc77  

For docker, see [scripts/install-docker.sh](../scripts/install-docker.sh).

### polkadot-deployer install and run
```
sudo npm i -g polkadot-deployer
polkadot-deployer --version
```
> 0.9.3  

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
at the moment still [results in this](https://github.com/w3f/polkadot-deployer/issues/5#issuecomment-499876296). Waiting for a solution ...


## issues
* [wpd#5](https://github.com/w3f/polkadot-deployer/issues/5) log files?

