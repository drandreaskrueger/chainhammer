# chainhammer substrate instructions

# installing

## substrate
Following https://substrate.dev/docs/en/getting-started/installing-substrate and -as usual lol- initially most manuals just don't work. Then after raising 2 [issues](#issues) (which were answered superfast!), this seems to be working:

```
git clone https://github.com/paritytech/substrate.git paritytech_substrate
cd paritytech_substrate
git checkout -b v1.0 origin/v1.0

./scripts/init.sh
./scripts/build.sh
cargo clean
RUSTFLAGS=-Awarnings cargo build --release
RUSTFLAGS=-Awarnings cargo build --release -p subkey

ls target/release/{subkey,substrate} -lh
sudo ln -s ~/Code/paritytech_substrate/target/release/substrate /usr/local/bin/
sudo ln -s ~/Code/paritytech_substrate/target/release/subkey /usr/local/bin/
subkey --version; substrate --version
```
> subkey 1.0.0  
> substrate 1.0.0-2f1b89f4-x86_64-linux-gnu  

syncing (by default "Chain specification: Emberic Elm")

    substrate
    
while watching the size on disk

    watch -n 10 "df|grep sda8; du ~/.local/share/substrate -d 0 -h"

Only the first THIRD of the chain already takes up 14 GB! My disk is small, so I quit syncing. After CTRL-C and restart, the size of ~/.local/share/substrate is suddenly 4.2G only. How to trigger that compression DURING syncing? Asked in chat.

## wabt
the suggested `apt install wabt` did not work (on Debian?), so build from source:
```
git clone --recursive https://github.com/WebAssembly/wabt WebAssembly_wabt
cd WebAssembly_wabt/
make
sudo make install
which wasm2c
ls bin/
```
playing with it:
```
nano test.wat
(module
  (func (export "addTwo") (param i32 i32) (result i32)
    local.get 0
    local.get 1
    i32.add))
```
```
bin/wat2wasm test.wat -o test.wasm; cat test.wasm
bin/wat2wasm test.wat -v
bin/wast2json test.wat -o test.json; cat test.json; cat test.0.wasm
bin/wasm2c test.wasm
bin/wasm-interp test.wasm --run-all-exports 
bin/wasm2c test.wasm -o test.c; cat test.c test.h
```

## ink!
Partially following https://substrate.dev/docs/en/contracts/installing-ink but with `wabt` from above.
```
cargo install pwasm-utils-cli --bin wasm-prune
cargo install --force --git https://github.com/paritytech/ink cargo-contract
cargo contract -V
cargo contract --help
```
> cargo-contract 0.1.1  



# other places

Mine - also see 

* [polkadot.md](polkadot.md)

External: See

* [Substrate on github/paritytech](https://github.com/paritytech/substrate)
* [Contracts module of the Substrate Module Runtime Library (SRML)](https://github.com/paritytech/substrate/tree/master/srml/contracts)
* [Introduction to Smart Contracts on Substrate](https://substrate.dev/docs/en/contracts/)
* chat [#substrate-technical:matrix.org](https://riot.im/app/#/room/#substrate-technical:matrix.org)

# issues
* [ps#3066](https://github.com/paritytech/substrate/issues/3066) no ./scripts/build.sh anymore 
* [ps#3067](https://github.com/paritytech/substrate/issues/3067) cargo build -> librocksdb-sys v5.14.2 -> unable to find libclang ... libclang.so
* [Ww#1106](https://github.com/WebAssembly/wabt/issues/1106) bin/wasm2c --version # how to ?


