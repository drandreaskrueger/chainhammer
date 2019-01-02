
echo
echo installing go and geth
echo 
read -p "Press enter to continue"

# would be nice to simply use geth via docker
# but this does not work yet:
# docker run ethereum/client-go attach https://localhost:8545
# please help
# until then, compile and install locally:

echo 
INSTALLER="go1.11.linux-amd64.tar.gz"
echo install go $INSTALLER
rm -f $INSTALLER
wget https://dl.google.com/go/$INSTALLER
sudo tar -C /usr/local -xzf $INSTALLER 
rm $INSTALLER  
mkdir -p ~/go/bin
echo "export PATH=\$PATH:/usr/local/go/bin:~/go/bin" >> ~/.profile
export PATH=$PATH:/usr/local/go/bin:~/go/bin
go version

    

echo install geth
go get -d github.com/ethereum/go-ethereum
go install "github.com/ethereum/go-ethereum/cmd/geth"
geth version

