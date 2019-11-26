# substrate recipes
https://substrate.dev/recipes/

    git checkout 89de89d9958145956a50bfb7ff49b0104517f56d

fixing issue when cargo build didn't work 

use our Polkadot-JS Apps to interact with your locally running node

* https://polkadot.js.org/apps/#/explorer?rpc=ws://127.0.0.1:9944
* Registering custom types - Additional types used by runtime modules can be added when a new instance of the API is created. This is necessary if the runtime modules use types which are not available in the base Substrate runtime. https://polkadot.js.org/api/api/#registering-custom-types

Gave up when `cargo build` did not result in `kitchen-node`. 
Faulty instructions. Reported:


# issues
* https://github.com/substrate-developer-hub/recipes/issues/83#issuecomment-556960537 current package believes it's in a workspace when it's not 