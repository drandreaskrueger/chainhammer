# this is for Debian/Ubuntu 
# see https://kubernetes.io/docs/tasks/tools/install-kubectl/ for other systems

echo
echo installing kubernetes repo source, and kubectl
echo
read -p "Press enter to continue"

sudo apt-get update && sudo apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubectl

set -x
kubectl version
set +x



