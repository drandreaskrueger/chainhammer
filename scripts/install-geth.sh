GO_INSTALLER="go1.11.4.linux-amd64.tar.gz"

echo
echo installing go and geth
echo 
read -p "Press enter to continue"

# would be nice to simply use geth via docker
# but this does not work yet:
# docker run ethereum/client-go attach https://localhost:8545
# please help
#
# until then, compile and install geth locally:

echo 
echo install go $GO_INSTALLER
rm -f $GO_INSTALLER
wget https://dl.google.com/go/$GO_INSTALLER
sudo tar -C /usr/local -xzf $GO_INSTALLER
rm $GO_INSTALLER
mkdir -p ~/go/bin
echo "export PATH=\$PATH:/usr/local/go/bin:~/go/bin" >> ~/.profile
export PATH=$PATH:/usr/local/go/bin:~/go/bin
go version

    

echo install geth
go get -d github.com/ethereum/go-ethereum
go mod init
go install "github.com/ethereum/go-ethereum/cmd/geth"
geth version

