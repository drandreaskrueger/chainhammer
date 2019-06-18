# Chainhammer Polkadot instructions

## polkadot-deployer
### cloud
The previous version `polkadot-deployer` v0.9 had strange problems on my local Debian machine, so I also tried it on a cloud machine. I could actually replicate the problem on AWS, based on a Debian image "debian-stretch-hvm-x86_64-gp2-2019-05-14-84483" (for identical replication of the problems mentioned below **please use the exact same AMI "ami-0faa9c9b5399088fd"**). First install nodejs, npm, docker:

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

I had EACCES access rights problems (and actually for 4 ways of npm install: `npm i $PRG`, `npm i -g $PRG`, `sudo npm i $PRG`, `sudo npm i -g $PRG` = all 4 had -different- EACCESS problems!), until I used this:
```
mkdir ~/.npm-global
sudo chown -R $USER ~/.npm-global
npm config set prefix '~/.npm-global'

nano ~/.profile
    export PATH=~/.npm-global/bin:$PATH
source ~/.profile
```

better use swap as RAM might become scarce:
```
SWAPFILE=/swapfile && free -m && sudo swapoff -a && sudo dd if=/dev/zero of=$SWAPFILE bs=1M count=1000 && sudo chmod 600 $SWAPFILE && sudo mkswap $SWAPFILE && echo $SWAPFILE none swap defaults 0 0 | sudo tee -a /etc/fstab && sudo swapon -a && free -m
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


#### polkadot-deployer swap out kubernetes
Polkadot-deployer v0.9 previously used  *kubernetes-in-docker* `byscorp/kind`, and that had unsolveable problems (see issue [wpd#5](https://github.com/w3f/polkadot-deployer/issues/5)), seemingly because [bsycorp/kind-v1.13 causes problems in approx 1 out of 3 attemps to start it](https://github.com/bsycorp/kind/issues/22). When they did not come up with a solution ... eventually we [swapped it out for another one](https://github.com/w3f/polkadot-deployer/issues/7). That `kubernetes-sigs/kind` needed some initial testing ... install, newest go:
```
which go
sudo rm -rf /usr/local/go
wget https://dl.google.com/go/go1.12.6.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.12.6.linux-amd64.tar.gz 
go version
```
> go version go1.12.6 linux/amd64  

install like [described](https://github.com/kubernetes-sigs/kind#installation-and-usage)
```
GO111MODULE="on" go get sigs.k8s.io/kind@v0.3.0
```
it's a bit confused about its `bin` folder (ends up in `~/bin/go/bin/bin`), so let's simply softlink it, then it works

    ln -s $GOPATH/bin/kind $GOPATH/kind
    kind version

> v0.3.0  

now let's try it:

    kind create cluster

results in:

```
kind create cluster
Creating cluster "kind" ...
 ✓ Ensuring node image (kindest/node:v1.14.2) 🖼 
 ✓ Preparing nodes 📦 
 ✓ Creating kubeadm config 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
Cluster creation complete. You can now use the cluster with:
export KUBECONFIG="$(kind get kubeconfig-path --name="kind")"
kubectl cluster-info
```
```
export KUBECONFIG="$(kind get kubeconfig-path --name="kind")"
echo $KUBECONFIG 
~/.kube/kind-config-kind

kubectl cluster-info
Kubernetes master is running at https://localhost:34755
KubeDNS is running at https://localhost:34755/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

As suggested [here](https://github.com/w3f/polkadot-deployer/issues/7#issuecomment-501762050), also trying out `helm`:

    sudo apt install snapd
    sudo snap install helm --classic

then
```
snap run helm init

$HELM_HOME has been configured at ~/.helm.
Tiller (the Helm server-side component) has been installed into your Kubernetes Cluster.
Please note: by default, Tiller is deployed with an insecure 'allow unauthenticated users' policy.
To prevent this, run `helm init` with the --tiller-tls-verify flag.
For more information on securing your installation see: https://docs.helm.sh/using_helm/#securing-your-helm-installation
```
then
```
kubectl get pods --all-namespaces -w

NAMESPACE     NAME                                         READY   STATUS    RESTARTS   AGE
kube-system   coredns-fb8b8dccf-94d5c                      1/1     Running   0          13m
kube-system   coredns-fb8b8dccf-f24nv                      1/1     Running   0          13m
kube-system   etcd-kind-control-plane                      1/1     Running   0          12m
kube-system   ip-masq-agent-2sqwx                          1/1     Running   0          13m
kube-system   kindnet-t9xxz                                1/1     Running   1          13m
kube-system   kube-apiserver-kind-control-plane            1/1     Running   0          11m
kube-system   kube-controller-manager-kind-control-plane   1/1     Running   0          12m
kube-system   kube-proxy-jn66q                             1/1     Running   0          13m
kube-system   kube-scheduler-kind-control-plane            1/1     Running   0          12m
kube-system   tiller-deploy-765dcb8745-9l97m               1/1     Running   0          27s
```
this looks good, right?

power it down again with

     kind delete cluster

#### polkadot-deployer new version 0.10 preparations

remove old:
```
npm r -g polkadot-deployer
rm -rf ~/.config/polkadot-deployer
docker kill $(docker ps -q); docker rm $(docker ps -q -a)
docker system prune -a --volumes
```

install new:

### polkadot-deployer install and run
```
npm i -g polkadot-deployer
polkadot-deployer --version
```
> 0.10.2  


```
polkadot-deployer --help
polkadot-deployer list
docker system prune -a --volumes
docker system prune -a --volumes # yes, twice
```
with `testnet1.json`:
```
{
  "name": "testnet1",
  "type": "local",
  "nodes": 4
}
```
```
polkadot-deployer create --verbose --config testnet1.json
```

After one more iteration, *it finally worked*, see [wpd#7](https://github.com/w3f/polkadot-deployer/issues/7#issuecomment-502222660) issue, and the comments below.


#### troubleshooting with kubectl
Especially when not working, this is useful to look deeper into it. Install `kubectl`, here for Debian/Ubuntu (but [see this](https://kubernetes.io/docs/tasks/tools/install-kubectl/) for other systems):
```
sudo apt-get update && sudo apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubectl
kubectl version
```
> Client Version: version.Info{Major:"1", Minor:"14", GitVersion:"v1.14.3", GitCommit:"5e53fd6bc17c0dec8434817e69b04a25d8ae0ff0", GitTreeState:"clean", BuildDate:"2019-06-06T01:44:30Z", GoVersion:"go1.12.5", Compiler:"gc", Platform:"linux/amd64"}

(obsolete: for old version with `bsycorp/kind` then get the config file from port 10080 with `wget -O config http://localhost:10080/config`, then ...)

Now using the config file show status via `kubectl`
```
export KUBECONFIG=$(kind get kubeconfig-path --name=testnet1); echo $KUBECONFIG

kubectl get nodes
kubectl describe node testnet1-control-plane   
kubectl describe deployments -n kube-system
kubectl describe deployments -n kube-system tiller-deploy
```

See issue a [late comment of wpd#5](https://github.com/w3f/polkadot-deployer/issues/5#issuecomment-502769328) for example outputs.

#### polkadot-deployer benchmark
Initial problems. See issue [wpd#8](https://github.com/w3f/polkadot-deployer/issues/8) ("benchmark stuck?"). A simple test was  suggested, to just start and stop a mariadb container ... and it actually failed. So I raised an issue with the mariadb-on-docker people: [bdm#186](https://github.com/bitnami/bitnami-docker-mariadb/issues/186).


## issues
* [wpd#5](https://github.com/w3f/polkadot-deployer/issues/5) log files?
* [bk#22](https://github.com/bsycorp/kind/issues/22) bsycorp/kind works only when started twice
* [wpd#7](https://github.com/w3f/polkadot-deployer/issues/7) choose different kubernetes-in-docker solution
* [wpd#8](https://github.com/w3f/polkadot-deployer/issues/8) benchmark stuck?
* [bdm#186](https://github.com/bitnami/bitnami-docker-mariadb/issues/186) mkdir: cannot create directory '/bitnami/mariadb/data': Permission denied
