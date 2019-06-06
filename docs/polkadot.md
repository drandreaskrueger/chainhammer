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
polkadot-deployer create --config testnet1.json
```
with `testnet1.json`:
```
{
  "name": "testnet1",
  "type": "local",
  "nodes": 4
}
```


## issues
* [wpd#5](https://github.com/w3f/polkadot-deployer/issues/5) log files?