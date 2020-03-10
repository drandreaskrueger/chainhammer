# substrate - signing transactions

## substrate subkey command 

As long as the polkascan library is still "read only" we must use `subkey` to sign transactions.

Turns out it has a bug: [pts#5180](https://github.com/paritytech/substrate/issues/5180) see below.

And the `sign-transaction` subcommand is the "missing chapter" in the documentation https://substrate.dev/docs/en/ecosystem/subkey#signing-and-verifying-messages . 

Until that is solved, I can also not continue with this: [pspsi#8](https://github.com/polkascan/py-substrate-interface/issues/8) see below.

Tried a "dirty hack" [going back to an old version of subkey](https://github.com/paritytech/substrate/issues/5180#issuecomment-596093813), and narrowed down the problem to [pspsi#9](https://github.com/polkascan/py-substrate-interface/issues/9) ? See [#issues](#issues) below.

... plenty of issues, chat, ...

#### nope:

Surprising [outcome](https://github.com/polkascan/py-substrate-interface/issues/9#issuecomment-597251575) is that `subkey sign-transaction...` is NOT to be used: "... has not been maintain over a year and we were recommended not to use this option of subkey."  

Weird. I would not have expected THAT. Zombie code just lying around to confuse newbies ;-)
  
But anyways, the good news is: Instead, I finally got the needed hints how to sign transactions with a completely different approach. Slow javascript not fast rust BUT IT WORKS, hooray:  

## polkadot JS wrappers

Two tools suggested: https://riot.im/app/#/room/!HzySYSaIhtyWrwiwEV:matrix.org/$1583872903119890zUuac:matrix.parity.io

### txwrapper

As for this there is only [JS documentation](https://github.com/paritytech/txwrapper/blob/master/docs/modules/_createsignedtx_.md) but no CLI example ... I have not tried it out; also Shawn didn't know; but [judging by the code](https://riot.im/app/#/room/#polkadot-watercooler:matrix.org/$1583880095252215PsOKK:matrix.org), it is [perhaps not faster](https://riot.im/app/#/room/#polkadot-watercooler:matrix.org/$1583882351257282PsbPW:matrix.org) than the "`signer sign`" tool anyways? -->

### signer sign
[dockerized](https://riot.im/app/#/room/#polkadot-watercooler:matrix.org/$1583879162249967usiRQ:matrix.org) is ~three times faster(!) than a [nondocker local install](https://riot.im/app/#/room/#polkadot-watercooler:matrix.org/$1583879105249853RnyOc:matrix.org).  Example call:

```
import substrateinterface
substrate = substrateinterface.SubstrateInterface(url="ws://127.0.0.1:9944/")
BOB_ADDRESS = '5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty'
payload = substrate.compose_call(call_module='Balances',
                                 call_function='transfer',
                                 call_params={'dest': BOB_ADDRESS,
                                              'value': 1000000000000})
print (payload)
```
> 0xa8040400ff8eaf04151687736326c9fea17e25fc5287613693c912909cb226aa4794f26a48070010a5d4e8

then 

```
time docker run jacogr/polkadot-js-tools signer sign --type sr25519 --account //Alice --seed "//Alice" 0xa8040400ff8eaf04151687736326c9fea17e25fc5287613693c912909cb226aa4794f26a48070010a5d4e8
```
> Signature: 0x01eab439c9fb689837b6e731413796037b09aa4d258205ba84cde63f22b4cc131f41117081ee73e508783c305dd6cbd79177889085d6d98c087637fbae261c8d88

> real	0m1.523s  
> user	0m0.033s  
> sys	0m0.018s  


## issues
* [pts#5180](https://github.com/paritytech/substrate/issues/5180) subkey sign-transaction = panicked `Option::unwrap()` on a `None` value
* [pspsi#8](https://github.com/polkascan/py-substrate-interface/issues/8) compose_call only works with dest=PUB_KEY
* [pspsi#9](https://github.com/polkascan/py-substrate-interface/issues/9) compose_call() results in payload that makes sign-transaction crash
* [pspsi#10](https://github.com/polkascan/py-substrate-interface/issues/10) signing transactions

