# chainhammer substrate v2 install instructions
This tutorial is uptodate (March 2020): https://substrate.dev/docs/en/overview/getting-started

I did the following, and it worked. 

Recorded so verbose, so that it can [later become an `install-node-template.sh` script](../scripts/).

### rust update; node & yarn correct versions
```
sudo apt update
sudo apt install -y cmake pkg-config libssl-dev git gcc build-essential git clang libclang-dev
source ~/.cargo/env # made it part of ~/.bashrc anyways
rustup update
rustup default stable
rustup update nightly
rustup target add wasm32-unknown-unknown --toolchain nightly
rustup --version; rustc --version; node --version; nodejs --version; yarn --version
```
> rustup 1.21.1 (7832b2ebe 2019-12-20)  
> rustc 1.41.1 (f3e1a954d 2020-02-24)  
> v11.15.0  
> v10.19.0  
> 1.22.0  

### substrate v2 stable pre-v2.0-3e65111:
later only subkey is needed, but this also installs the default `substrate` binary:
```
git clone https://github.com/paritytech/substrate/ paritytech_substrate_v2
cd paritytech_substrate_v2/
git checkout 3e65111
cargo clean
nice cargo build --release # perhaps drop this, as below 'install' compiles anyways?
cargo test --release --all # perhaps drop this. All but 2 tests are passing.

# install into ~/.cargo/bin:
nice cargo install --force --path ./bin/node/cli/ 
nice cargo install --force --path ./bin/utils/subkey subkey
# always keep versions
version=$(target/release/substrate --version | awk '{ print $2 }' )
pushd ~/.cargo/bin
mv substrate substrate-$version
mv subkey subkey-$version
ln -s substrate-$version substrate 
ln -s subkey-$version subkey
ls -latr sub*
popd
which substrate; which subkey # just to be sure
substrate --version; subkey --version
```
> version 2.0.0-3e651110a-x86_64-linux-gnu  

### node-template v2 (on basis of same substrate stable pre-v2.0-3e65111):
`node-template` is a "minimal working Substrate node meant for the development of new Substrate blockchains":
```
git clone https://github.com/substrate-developer-hub/substrate-node-template substrate-developer-hub_substrate-node-template_v2
cd substrate-developer-hub_substrate-node-template_v2/
git checkout 8b6fe666
nice cargo build --release
version=$(target/release/node-template --version | awk '{ print $2 }' )
cp ./target/release/node-template ~/.cargo/bin/node-template-$version
ln -s ~/.cargo/bin/node-template-$version ~/.cargo/bin/node-template
ls -latr ~/.cargo/bin/node*
which node-template
node-template --version
```
> version 2.0.0-8b6fe66-x86_64-linux-gnu

start new chain:
```
node-template purge-chain -y --dev
node-template --dev
```

keep it running, and either https://polkadot.js.org/apps/#/settings --> `127.0.0.1:9944` OR in new terminal:
### frontend sdh-sfet 006ef1c2
```
git clone https://github.com/substrate-developer-hub/substrate-front-end-template substrate-developer-hub_substrate-front-end-template_v2
cd substrate-developer-hub_substrate-front-end-template_v2
git checkout 006ef1c2
yarn install
yarn start
```
> http://localhost:8000/

### Store a value in the chain:
http://localhost:8000/ --> Store something.   

Or 

* [WRITE extrinsic](https://polkadot.js.org/apps/#/extrinsics) ALICE --> templateModule --> doSomething(something) --> 42 --> Submit.  
* [READ chainstate](https://polkadot.js.org/apps/#/chainstate) --> templateModule -->  something() --> PLUS.  

It works!

---

---

---

#OLD:

All following is historical - left here only as lookup. Substrate v2 now had 'feature freeze'. Redone all this; see above.

However, perhaps check the [list of ISSUES at the bottom of the page](#issues).

---

Chapters:

* substrate 1.0
* wabt
* ink!
* [#alternative-installation-1](#alternative-installation-1)
* [#alternative-installation-2](#alternative-installation-2).
* substrate 2.0
* node template dev chain
* configure network: own keys & own chainspec
  * https://gitlab.com/andreaskrueger/substrate-starter

## substrate 1.0
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

Only the first THIRD of the chain already takes up 14 GB! My disk is small, so I quit syncing. After CTRL-C and restart, the size of ~/.local/share/substrate is suddenly 4.2G only. How to trigger that compression DURING syncing? Asked in chat. Answer: Pruning, probably faulty.

Good that issue came up now, because seeminly there is confusion which version ([v1.0 (see issue 3066)](https://github.com/paritytech/substrate/issues/3066#issuecomment-509371473) or [master (see issue 3077)](https://github.com/paritytech/substrate/issues/3107#issuecomment-510618402)) is right for me. Let's wait what they come up with.


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


# alternative installation 1
following these [workshop instructions](https://www.shawntabrizi.com/substrate-beginner-workshop/#/0/), but manually going through http://getsubstrate.io/ script:

## dependencies and rust and wasm

    sudo apt update
    sudo apt install -y cmake pkg-config libssl-dev git gcc build-essential git clang libclang-dev
	rustup update
	rustup default stable    
    rustup update nightly
    rustup target add wasm32-unknown-unknown --toolchain nightly
    command -v wasm-gc || cargo +nightly install --git https://github.com/alexcrichton/wasm-gc --force
    rustup --version; rustup toolchain list; rustup check

(wasm-gc is needed even though [its repo says it is no longer necessary](https://github.com/alexcrichton/wasm-gc#wasm-gc))

versions:

> rustup 1.20.2 (13979c968 2019-10-16)  
> stable-x86_64-unknown-linux-gnu (default)  
> nightly-x86_64-unknown-linux-gnu  
> stable-x86_64-unknown-linux-gnu - Up to date : 1.39.0 (4560ea788 2019-11-04)  
> nightly-x86_64-unknown-linux-gnu - Up to date : 1.40.0-nightly (bc0e288ad 2019-11-11)  


## substrate 2.0

    git clone https://github.com/paritytech/substrate paritytech_substrate
    cd paritytech_substrate
    cargo install --force --path ./node/cli       #substrate
    cargo install --force --path ./subkey subkey

versions on Nov 12th 2019 - master branch:

    substrate --version; subkey --version
    substrate 2.0.0-dc16bac5e-x86_64-linux-gnu
    subkey 2.0.0

Sadly there [doesn't seem to be a tagged v2.0... version yet](https://github.com/paritytech/substrate/issues/3066#issuecomment-553044382), so anything here can always break. Then this should bring you to the version that I am using for now: 

    git checkout dc16bac5e5ab289e3cd735a25aadaf2d562050cc

## substrate-up

    cd ..
    git clone https://github.com/paritytech/substrate-up paritytech_substrate-up
    cp -a paritytech_substrate-up/substrate-* ~/.cargo/bin
    cp -a paritytech_substrate-up/polkadot-* ~/.cargo/bin

versions: sorry no, the *code for that is missing* but the commit hash was 

    dcc2d521b6ba0ef4533dcc5cfc49ec290f9c62a9

And it looks like these 4 were copied; all bash scripts:

    cat polkadot-js-apps-new substrate-module-new substrate-node-new substrate-ui-new

## syncing main chain

syncing (by default "Chain specification: Flaming Fir")

    substrate
    
while watching the size on disk

    watch -n 10 "df|grep sda8; du ~/.local/share/substrate -d 0 -h"

Stuck at block #37939 - see [Polkadopt telemetry site](https://telemetry.polkadot.io/#list/Flaming%20Fir)


## node template dev chain

As in [workshop instructions](https://www.shawntabrizi.com/substrate-beginner-workshop/#/0/) but modified to fix version, and copy to PATH:

    git clone https://github.com/substrate-developer-hub/substrate-node-template substrate-developer-hub_substrate-node-template
    cd substrate-developer-hub_substrate-node-template
    git checkout 43ee95347b6626580b1d9d554c3c8b77dc85bc01
    cargo build --release
    cp -a ./target/release/node-template ~/.cargo/bin
    node-template --version

This was the version on November 12th 2019:  

> node-template 2.0.0-43ee953-x86_64-linux-gnu

## run node template

If everything completed successfully, you should see your local development node producing blocks:

    # node-template purge-chain --dev # use this to remove existing development chain
    node-template --dev

possibly run with more debug infos: 

    RUST_LOG=debug RUST_BACKTRACE=1 cargo run -- --dev


# TODO: standalone repo 'substrate-starter'
N.B.: Everything below is to be modified for the newly created standalone repo:

* https://gitlab.com/andreaskrueger/substrate-starter

which does EVERYTHING there with only two bash scripts `./init.sh; ./start.sh` !!!

## local network four nodes


* start: `networks/node-template_start-4-local-nodes.sh`
* kill: `networks/node-template_kill-all-nodes.sh`
* purge = delete chains: `networks/node-template_purge-4-local-nodes.sh`


# alternative installation 2
Wow, their tutorials are changing fast. This [issue comment](https://substrate.dev/docs/en/next/tutorials/start-a-private-network-with-substrate) gave me yet another entry point; this time getting rid of Alice Bob Charlie Dave, and using an individual chainspec instead.

## dependencies and compilation

rust:

    sudo apt update
    sudo apt install -y cmake pkg-config libssl-dev git gcc build-essential git clang libclang-dev
	rustup update
	rustup default stable    
    rustup update nightly
    rustup target add wasm32-unknown-unknown --toolchain nightly
    command -v wasm-gc || cargo +nightly install --git https://github.com/alexcrichton/wasm-gc --force
    rustup --version; rustup toolchain list; rustup check

versions:

> rustup 1.20.2 (13979c968 2019-10-16)  
> stable-x86_64-unknown-linux-gnu - Up to date : 1.39.0 (4560ea788 2019-11-04)  
> nightly-x86_64-unknown-linux-gnu - Up to date : 1.40.0-nightly (4f03f4a98 2019-11-12)  

substrate subkey and node-template:

```
git clone https://github.com/paritytech/substrate paritytech_substrate
cd paritytech_substrate
git checkout 7d7e74fb

cargo install --force --path subkey subkey
cd node-template
cargo build --release

mv ../target/release/node-template ~/.cargo/bin/node-template-2.0.0-7d7e74fb7
ln -s ~/.cargo/bin/node-template-2.0.0-7d7e74fb7 ~/.cargo/bin/node-template

node-template --version; subkey --version
```
versions:

> node-template 2.0.0-7d7e74fb7-x86_64-linux-gnu  
> subkey 2.0.0 # better here include the commit hash too?  


ui:

```
cd ../..
git clone https://github.com/polkadot-js/apps polkadot-js_apps
cd polkadot-js_apps
yarn
yarn run start
```
http://localhost:3000

## configure network

### own keys & own chainspec

I suggest paritytech makes this whole procedure into a (better than mine) scripted automatism 
INCL already inserting the generated keys into an own chainspec. My 3 scripts are a good start:

      node-template_chainspec-generate.sh 4

does this:

1. generate 4 seeds in `subkey_gen-seeds.sh`
2. convert 4 seeds into `babe` (or `grandpa`) keys in json lists via `subkey_keys-from-seeds.sh 4 babe`
3. generates a local.json from `node-template --chain local`
4. inputs the keys from (2.), into a CH.json
5. turns that into a CH-raw.json 


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
* [ps#3107](https://github.com/paritytech/substrate/issues/3107) no pruning ?
* [ps#4096](https://github.com/paritytech/substrate/issues/4096) error: The argument '--name <NAME>' cannot be used with '--dave'
* [ps#4103](https://github.com/paritytech/substrate/issues/4103) --node-key vs --node-key-file 
* [sdh#327](https://github.com/substrate-developer-hub/substrate-developer-hub.github.io/issues/327) suggestion what to add to 'start-a-private-network-with-substrate'
* [#sdh#473](https://github.com/substrate-developer-hub/substrate-developer-hub.github.io/issues/473) v2 tutorials?
* [#sdh#474](https://github.com/substrate-developer-hub/substrate-developer-hub.github.io/issues/474)  v2 installing-substrate#manual-build
* [#sdht#24](https://github.com/substrate-developer-hub/substrate-node-template/issues/24) v2 ready ?
* [#sdh#476](https://github.com/substrate-developer-hub/substrate-developer-hub.github.io/issues/476) cargo test --release --all ?

