echo
echo compile and install geth
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
go get -d github.com/ethereum/go-ethereum
go install "github.com/ethereum/go-ethereum/cmd/geth"
geth version

