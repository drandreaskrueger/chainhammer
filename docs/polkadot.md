# Chainhammer Polkadot instructions

## polkadot-deployer
polkadot-deployer is a very useful tool that starts a polkadot network with e.g. 4 nodes. 

It is using kubernetes which causes quite some problems (on Debian?). The first parts of this file here (and the below first 5 [issues](#issues) on github) are dedicated to finding out what's wrong. To avoid any idiosyncrasies of my *local* machine, I succesfully replicated the problem on a *standard cloud machine based on Debian*:

### cloud
(for more detailed instructions how to connect to AWS machines, [see cloud.md](cloud.md#aws-deployment))

Avoid all these installations by using my ready-made public Amazon AMI [ami-0aa7c32c39edb5062, and you can create an instance from that](https://eu-west-2.console.aws.amazon.com/ec2/v2/home?region=eu-west-2#Images:search=ami-0aa7c32c39edb5062), and then directly continue below in chapter [polkadot-deployer create](#polkadot-deployer-create).

**OR**

Create your own AWS machine based on a Debian image "debian-stretch-hvm-x86_64-gp2-2019-05-14-84483" (for identical replication of the problems mentioned below **please use the exact same AMI "ami-0faa9c9b5399088fd"**).  
**AWS**: [launch instance](https://eu-west-2.console.aws.amazon.com/ec2/v2/home?region=eu-west-2#LaunchInstanceWizard), community AMIs, debian-stretch-hvm-x86_64-gp2-2019-05-14-84483, t2.medium, ... wait until booted, then connect with ssh.

First install nodejs, npm, go, kubectl, swap, docker:

```
sudo apt install -y git snapd
git clone https://github.com/drandreaskrueger/chainhammer
cd chainhammer
git checkout polkadot

scripts/install-nodejs.sh 
scripts/install-go.sh 
scripts/install-kubernetes.sh 
scripts/create-swap.sh 
scripts/install-docker.sh 

exit
```
logout and log back in, so that $USER is in docker group:
```
ssh chainhammer
groups; docker --version
  admin adm [...] docker
  Docker version 18.09.6, build 481bc77
```

situation:
```
nodejs --version; node --version; npm --version; go version; docker --version; free -m; df -h

v10.16.0
v10.16.0
6.9.0

go version go1.12.6 linux/amd64

Docker version 18.09.6, build 481bc77

              total        used        free      shared  buff/cache   available
Mem:           3954          99        1015           7        2839        3567
Swap:           999           0         999

Filesystem   I have created a public Amazon AMI from this, so that you don't *have to do* the above steps.
The AMI is called [ami-0aa7c32c39edb5062, and you can create an instance from that](https://eu-west-2.console.aws.amazon.com/ec2/v2/home?region=eu-west-2#Images:search=ami-0aa7c32c39edb5062), and then directly continue here:   Size  Used Avail Use% Mounted on
/dev/xvda1      7.9G  3.3G  4.2G  44% /
```

**polkadot-deployer swap out kubernetes:** Polkadot-deployer v0.9 previously used  *kubernetes-in-docker* `byscorp/kind`, and that had unsolveable problems (see issue [wpd#5](https://github.com/w3f/polkadot-deployer/issues/5)), seemingly because [bsycorp/kind-v1.13 causes problems in approx 1 out of 3 attemps to start it](https://github.com/bsycorp/kind/issues/22). When they did not come up with a solution ... eventually we [swapped it out for another one](https://github.com/w3f/polkadot-deployer/issues/7). That new `kubernetes-sigs/kind` ... install like [described here](https://github.com/kubernetes-sigs/kind#installation-and-usage); it's a bit confused about its `bin` folder (ends up in `~/bin/go/bin/bin`), so let's simply softlink it, then it works.
```
GO111MODULE="on" go get sigs.k8s.io/kind@v0.3.0
ln -s $GOPATH/bin/kind $GOPATH/kind
kind version
```
> v0.3.0    ami-0aa7c32c39edb5062

we [also need](https://github.com/w3f/polkadot-deployer/issues/7#issuecomment-501762050) `helm` (logout and log back in to use):

    sudo snap install helm --classic

now let's try it (for details see [this and the following comments in issue wpd#8](https://github.com/w3f/polkadot-deployer/issues/8#issuecomment-503054700)).

#### Amazon IMAGE !

I have created a public Amazon AMI from this, so that you don't *have to do* the above steps.
The AMI is called [ami-0aa7c32c39edb5062, and you can create an instance from that](https://eu-west-2.console.aws.amazon.com/ec2/v2/home?region=eu-west-2#Images:search=ami-0aa7c32c39edb5062), and then directly continue here:

### polkadot-deployer create

    npm i -g polkadot-deployer
    polkadot-deployer --version

> 0.10.4

now works:

    polkadot-deployer create --config networks/polkadot-testnet1.json

(use --verbose if any problems).

### polkadot-deployer benchmark
but

    polkadot-deployer benchmark --verbose -c networks/polkadot-finality1.json 

... still has unsolved initial problems. See issue [wpd#8](https://github.com/w3f/polkadot-deployer/issues/8) ("benchmark stuck?"). A simple test was  suggested, to just start and stop a mariadb container:

```
kind create cluster
export KUBECONFIG="$(kind get kubeconfig-path --name=kind)"; echo $KUBECONFIG

helm init
helm init --upgrade

kubectl create serviceaccount --namespace kube-system tiller
kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
kubectl patch deploy --namespace kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'
kubectl get pods --all-namespaces | grep tiller

helm install --name mariadb --set master.persistence.enabled=false --set slave.persistence.enabled=false stable/mariadb
kubectl get pods -w --all-namespaces 
```

testing whether "terminate" works:

    helm delete --purge mariadb
    kubectl get pods -w --all-namespaces | grep maria
    
    default       mariadb-master-0                             0/1     Terminating   0          3m5s
    default       mariadb-slave-0                              0/1     Terminating   0          3m5s

It does not. It keeps on saying "Terminating", even after many minutes.

Power it down again, and remove as much leftovers as possible:

```
kind delete cluster
docker kill $(docker ps -q); docker rm $(docker ps -q -a)
docker system prune -af --volumes
```
we have to wait what comes out of this issue [wpd#8](https://github.com/w3f/polkadot-deployer/issues/8).



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
Especially when not working, this is useful to look deeper into it. 
```
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




## issues
* [wpd#5](https://github.com/w3f/polkadot-deployer/issues/5) log files?
* [bk#22](https://github.com/bsycorp/kind/issues/22) bsycorp/kind works only when started twice
* [wpd#7](https://github.com/w3f/polkadot-deployer/issues/7) choose different kubernetes-in-docker solution
* [wpd#8](https://github.com/w3f/polkadot-deployer/issues/8) benchmark stuck?
* [bdm#186](https://github.com/bitnami/bitnami-docker-mariadb/issues/186) mkdir: cannot create directory '/bitnami/mariadb/data': Permission denied
