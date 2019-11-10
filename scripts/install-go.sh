GO_INSTALLER="go1.13.4.linux-amd64.tar.gz"

echo
echo installing golang version $GO_INSTALLER
echo NB: any problems, try to move folder /usr/local/go and examine ~/.profile
echo
read -p "Press enter to continue"

echo 
echo install go $GO_INSTALLER
rm -f $GO_INSTALLER
wget https://dl.google.com/go/$GO_INSTALLER
sudo tar -C /usr/local -xzf $GO_INSTALLER
rm $GO_INSTALLER

echo creating folder ~/go and adding to ENV
mkdir -p ~/go/bin
echo "export PATH=\$PATH:/usr/local/go/bin:~/go/bin" >> ~/.profile
echo "export GOPATH=~/go" >> ~/.profile
export PATH=$PATH:/usr/local/go/bin:~/go/bin
export GOPATH=~/go

go version
