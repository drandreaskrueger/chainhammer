# parity
what I found out about using parity and parity-deploy is either here, on in [../results/parity.md](../results/parity.md).

## quickstart
while helping to debug parity's great tool parity-deploy 
(e.g. [here](https://github.com/paritytech/parity-deploy/issues/76)), 
these mini-scripts turned out to be useful for testing:

### parity instantseal

```
PARITY_VERSION=v2.2.3
sudo rm -rf paritytech_parity-deploy
git clone https://github.com/paritytech/parity-deploy.git paritytech_parity-deploy
cd paritytech_parity-deploy
git log | head -n 5 
git checkout 1a6afd17ac75bdf6c9e9fefa1d3af13748dd9cfa

sudo ./clean.sh
./parity-deploy.sh -r $PARITY_VERSION --config dev --geth
sed -i 's/parity:stable/parity:'$PARITY_VERSION'/g' docker-compose.yml
docker-compose up
```

```
PARITY_VERSION=v1.11.11
#sudo rm -rf paritytech_parity-deploy
#git clone https://github.com/paritytech/parity-deploy.git paritytech_parity-deploy
#cd paritytech_parity-deploy
#git log | head -n 5 
#git checkout 1a6afd17ac75bdf6c9e9fefa1d3af13748dd9cfa
sudo ./clean.sh
sudo rm $(which parity)
./parity-deploy.sh -r $PARITY_VERSION --config dev --geth
sed -i 's/user:\ parity/user:\ root/g' docker-compose.yml 
sed -i 's/parity:stable/parity:'$PARITY_VERSION'/g' docker-compose.yml
docker-compose up
```


### parity aura

```
PARITY_VERSION=v2.2.3
#sudo rm -rf paritytech_parity-deploy
#git clone https://github.com/paritytech/parity-deploy.git paritytech_parity-deploy
#cd paritytech_parity-deploy
#git checkout 1a6afd17ac75bdf6c9e9fefa1d3af13748dd9cfa
sudo ./clean.sh
./parity-deploy.sh -r $PARITY_VERSION --config aura --nodes 4 --geth
sed -i 's/parity:stable/parity:'$PARITY_VERSION'/g' docker-compose.yml
docker-compose up
```

```
PARITY_VERSION=v1.11.11
#sudo rm -rf paritytech_parity-deploy
#git clone https://github.com/paritytech/parity-deploy.git paritytech_parity-deploy
#cd paritytech_parity-deploy
#git checkout 1a6afd17ac75bdf6c9e9fefa1d3af13748dd9cfa
sudo ./clean.sh
sudo rm $(which parity)
./parity-deploy.sh -r $PARITY_VERSION --config aura --nodes 4 --geth
sed -i 's/user:\ parity/user:\ root/g' docker-compose.yml 
sed -i 's/parity:stable/parity:'$PARITY_VERSION'/g' docker-compose.yml
docker-compose up
```

## issues
scroll down on [../results/parity.md --> issues](../results/parity.md#issues) to find a long list of parity-related issues that I collaborated in.

