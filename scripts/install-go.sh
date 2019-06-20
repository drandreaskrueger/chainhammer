GO_INSTALLER="go1.12.6.linux-amd64.tar.gz"

echo
echo installing golang version $GO_INSTALLER
echo
read -p "Press enter to continue"

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



