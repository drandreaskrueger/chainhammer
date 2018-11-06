# chainhammer FAQ
frequently asked questions, explaining approach, or code
---

## send via `web3.py` versus send via direct RPC call 'eth_sendTransaction`
 
This question was asked here: https://github.com/paritytech/parity-ethereum/issues/9393#issuecomment-436294454

> because the web3 library is too slow

Yes, for low (two digit) TPS it does not make a big difference, only ~20% faster. But when I get into the hundreds of TPS, I see considerable gains (~ twice as fast) when bypassing web3 completely.  Please have a quick look at these old experiments: https://github.com/drandreaskrueger/chainhammer/blob/master/log.md#sending-via-web3-versus-sending-via-rpc

---


> basically pre-signing 

Not sure we are talking about the same thing actually. Even when bypassing the web3.py library, I am using the RPC `method = 'eth_sendTransaction`.


Have a look at these two codepieces:

### via web3  

in https://github.com/drandreaskrueger/chainhammer/blob/93c40384a4d178bdb00cea491d15b14046471b72/send.py#L73-L93   
it is simply this one liner https://github.com/drandreaskrueger/chainhammer/blob/93c40384a4d178bdb00cea491d15b14046471b72/send.py#L90

while 

### via RPC

in https://github.com/drandreaskrueger/chainhammer/blob/93c40384a4d178bdb00cea491d15b14046471b72/send.py#L106-L183
I am doing (`contract_method_ID` + `argument_encoding` --> `payload`), then (plus `headers` into a`requests.post` to call `eth_sendTransaction`), see here:  
https://github.com/drandreaskrueger/chainhammer/blob/93c40384a4d178bdb00cea491d15b14046471b72/send.py#L178


### choice

I switch between those two routes here https://github.com/drandreaskrueger/chainhammer/blob/93c40384a4d178bdb00cea491d15b14046471b72/send.py#L201

choice constant `ROUTE` is defined in config.py

---

