# chainhammer substrate instructions

# installing
Following https://substrate.dev/docs/en/getting-started/installing-substrate and -as usual lol- initially most manuals just don't work. Then after raising 2 [issues](#issues) (which were answered superfast!), this seems to be working:

```
git clone https://github.com/paritytech/substrate.git paritytech_substrate
cd paritytech_substrate

git checkout -b v1.0 origin/v1.0
./scripts/init.sh
./scripts/build.sh
cargo clean
RUSTFLAGS=-Awarnings cargo build
RUSTFLAGS=-Awarnings cargo build -p subkey
```


# other places

Mine - also see 

* [polkadot.md](polkadot.md)

External: See

* [Substrate on github/paritytech](https://github.com/paritytech/substrate)
* [Contracts module of the Substrate Module Runtime Library (SRML)](https://github.com/paritytech/substrate/tree/master/srml/contracts)
* [Introduction to Smart Contracts on Substrate](https://substrate.dev/docs/en/contracts/)

# issues
* [ps#3066](https://github.com/paritytech/substrate/issues/3066) no ./scripts/build.sh anymore 
* [ps#3067](https://github.com/paritytech/substrate/issues/3067) cargo build -> librocksdb-sys v5.14.2 -> unable to find libclang ... libclang.so
