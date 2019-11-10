GETH_VERSION=v1.9.6

echo
echo compile and install geth $GETH_VERSION
echo 
read -p "Press enter to continue"

# would be nice to simply use geth via docker
# but this does not work yet:
# docker run ethereum/client-go attach https://localhost:8545
# please help
#
# until then, compile and install geth locally:

go version

echo get, compile and install geth - patience please
echo

echo download repo into $GOPATH
go get -d -u github.com/ethereum/go-ethereum
echo

# set to a specific version
echo checkout repo to specific geth version $GETH_VERSION
OLDPATH=$(pwd)
cd $GOPATH/src/github.com/ethereum/go-ethereum/
git checkout $GETH_VERSION
cd $OLDPATH
echo	

echo remove the old geth binary
rm -f $(which geth)

echo force rebuild geth command ethereum/go-ethereum/cmd/geth
go clean -r "github.com/ethereum/go-ethereum/cmd/geth"
go install  "github.com/ethereum/go-ethereum/cmd/geth"

geth version

