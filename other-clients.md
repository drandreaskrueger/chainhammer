# other clients
Purpose: Extending this to benchmark other Ethereum-type chains

### start node
    
parity Toabalaba energywebfoundation

     ./target/release/parity --geth --chain tobalaba --rpcapi "web3,eth,personal"
     

parity main chain (untested):

    parity --geth --rpcapi "web3,eth,personal"

    
### account, password

By default, the [deploy.py](deploy.py) uses the first address `web3.eth.accounts[0]`.    
Put your `unlockAccount` passphrase into the file `account-passphrase.txt` (the passphrase must not have whitespaces at the beginning or end).  

