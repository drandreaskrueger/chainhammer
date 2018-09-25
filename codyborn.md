# CodyBorn's benchmarking

## perhaps working, but exotic:

About the 'nonsimple ( * ) idea' remark in '[Please you help](https://gitlab.com/electronDLT/chainhammer/blob/master/parity.md#please-you-help)'...:

There *seems to be* an exotic way of talking to an Ethereum node, bypassing a lot of the (possibly uncleverly implemented) parity code like transaction signing, and nonce-handling ... A microsoft employee has recently set up a benchmarking on Azure, to push the limits further. 

His approach is incompatible with mine, as I am sending all transactions from the same account, and let `geth` or `parity` handle the nonce lookup and signing. 

Cody Born's approach seems to be similar as in:

* he sends a simple contract state update

but different in at least:

* no verification of a majority of transactions
* each transaction comes from a different account
  * he signs the transactions himself (!)
  * he handles the nonces himself (!)

For details, we have to wait until he publishes his code. So far he told us this:

### CodyBorn Microsoft

Cody Born did parity benchmarking on Azure, and reached a TPS almost as fast as [geth](geth.md) ("400 TPS"):

> Cody Born @codyborn  
> @ParityTech Proof-of-Authority is fast! ⚡️  
> Using Ethereum on @Azure, I measured an average 400 TPS with a peak of 1700 TPS using a simple perf tool I put together.    
> Results are measured on an Ethereum chain deployed across West US and East US.  
> https://docs.microsoft.com/en-us/azure/blockchain-workbench/ethereum-poa-deployment

see
> https://twitter.com/codyborn/status/1040081548135948288  

the description at [https://docs.microsoft...](https://docs.microsoft.com/en-us/azure/blockchain-workbench/ethereum-poa-deployment) is incomplete; i.e. his benchmarking code itself is still closed source, but we found out this already:

> Cody Born  
> 3 days ago  
> Replying to @drandreaskruger    
> We'll be publishing our tool and methodology soon to a public GitHub repo.  
> I'll DM you more details.   
> I would also try using our Ethereum POA deployment in Azure as a starting point to replicate the environment I used to isolate the changes.  
> https://twitter.com/codyborn/status/1043533344271556609  

and in a direct message to me:

> Sep 22  
> For my tests I'm performing a simple contract state update   
> where each transaction comes from a different account.  
> I verify only a small percentage of the transactions to reduce load on the machines.  
> Also make sure the gas limit is not the current bottleneck.  

However, if all transaction then are sent from the same account I would have conflicts of wrong nonces if I send transactions multi-threaded - so I cannot use Cody's approach without massive changes to my simple benchmarking code.

Cody writes in another DM:


> Cody Born
> Using different accounts ensures that nonce ordering is not a bottleneck.  
> Sep 22    

So my current chainhammer-code -which works fast with `geth` but slow with `parity`- would not be able to do the same. For my 20,000 transactions I am not using 20,000 different accounts, but 1 account.


#### Most important experiment that CodyBorn could do:

Replicate his exact approach but using `geth clique`, see [geth.md#results](geth.md#results).



