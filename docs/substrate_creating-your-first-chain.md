# Creating Your First Substrate chain
following https://substrate.dev/docs/en/tutorials/creating-your-first-substrate-chain

## dependencies

```
sudo npm cache clean -f
sudo npm install -g n
sudo n v11.15.0
npm install -g npm
sudo npm install -g npm

node --version; npm --version
```
> v11.15.0
> 6.13.0

Must be older version 11 see issue: [sdh#8](https://github.com/substrate-developer-hub/substrate-node-template/issues/8)


install substrate https://substrate.dev/docs/en/getting-started/installing-substrate

    substrate --version; subkey --version

> substrate 2.0.0-dc16bac5e-x86_64-linux-gnu  
> subkey 2.0.0  

presentation "Getting Started on Substrate" https://docs.google.com/presentation/d/1dhaoLb5V2K_vDe4EJlUcKwePD1nMktr57fOdSo8bHns/edit#slide=id.g45ee0ba2ab_3_12

following the tutorial ...

```
substrate-node-new substrate-node-template chainhammer
...
Chain client created in substrate-node-template.
To start a dev chain, run:
$ substrate-node-template/target/release/substrate-node-template --dev
To create a basic Bonds UI for your chain, run:
$ substrate-ui-new substrate-node-template
To push to a newly created GitHub repository, inside substrate-node-template, run:
$ git remote add origin git@github.com:myusername/myprojectname && git push -u origin master
```

```
substrate-ui-new substrate-node-template
cd substrate-node-template-ui
yarn run dev
```

following the tutorial ...

(Strg-Shift-J to see console)

runtime upgrade --> StyleStatus.finalized : 0xc4501c8a56cc634add41e5c139faeb428a336b712fa1195c1626a515163a979e

searching for that in log:

```
2019-11-17 10:40:40 Starting consensus session on top of parent 0x04ae287be3ba4547a78b2a17e9fc29cf2f30e22cd3db76a5cebe6036f36a3406
2019-11-17 10:40:40 Prepared block for proposing at 879 [hash: 0x8e974907f934390b385c15acf64bfd4d7192fb1ee70fd2fbe30f66dc20b614f9; parent_hash: 0x04ae…3406; extrinsics: [0x2edd…c245, 0x84ce…5651]]
2019-11-17 10:40:40 Pre-sealed block for proposal at 879. Hash now 0xc4501c8a56cc634add41e5c139faeb428a336b712fa1195c1626a515163a979e, previously 0x8e974907f934390b385c15acf64bfd4d7192fb1ee70fd2fbe30f66dc20b614f9.
2019-11-17 10:40:40 Imported #879 (0xc450…979e)
2019-11-17 10:40:43 Idle (0 peers), best: #879 (0xc450…979e), finalized #0 (0xc0d3…c522), ⬇ 0 ⬆ 0
2019-11-17 10:40:48 Idle (0 peers), best: #879 (0xc450…979e), finalized #0 (0xc0d3…c522), ⬇ 0 ⬆ 0
2019-11-17 10:40:50 Starting consensus session on top of parent 0xc4501c8a56cc634add41e5c139faeb428a336b712fa1195c1626a515163a979e
2019-11-17 10:40:50 Prepared block for proposing at 880 [hash: 0x069d5b46b546f4450a9ddf6837c0b3ff6ecea8c81e7913aa970ae9ecd784aabe; parent_hash: 0xc450…979e; extrinsics: [0xbe44…c81b]]
2019-11-17 10:40:50 Pre-sealed block for proposal at 880. Hash now 0x9408613555757106cea7502833b1f1399a4df1698e58cf791b62b10abc94b334, previously 0x069d5b46b546f4450a9ddf6837c0b3ff6ecea8c81e7913aa970ae9ecd784aabe.
2019-11-17 10:40:50 Imported #880 (0x9408…b334)
```

Then following the rest of that page. 

Apart from the small issues [sdh#9](https://github.com/substrate-developer-hub/substrate-node-template/issues/9) and [sdh#10](https://github.com/substrate-developer-hub/substrate-node-template/issues/10) all went well.  

I got it working as expected. Nice.


## issues:
* [sdh#8](https://github.com/substrate-developer-hub/substrate-node-template/issues/8) node 12
* [sdh#9](https://github.com/substrate-developer-hub/substrate-node-template/issues/9) no node_runtime.compact.wasm but substrate_node_template_runtime_wasm.compact.wasm
* [sdh#10](https://github.com/substrate-developer-hub/substrate-node-template/issues/10) impl_name: create_runtime_str!("demo-node"),