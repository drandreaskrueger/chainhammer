# substrate-collectables-workshop

https://substrate.dev/substrate-collectables-workshop

commit 408e902b0ba75839676069d5832762d13da038d2

## Possibly useful bits and pieces:

> build your own Substrate package by running:  
> `substrate-node-new <project_name> <your_name>` 
> `substrate-ui-new <project_name>`  
> As mentioned earlier, the one downside of this method is that these scripts pull directly from different GitHub repositories, which means there may be times of incompatibility during breaking changes.

> When building your own UI, you can refer to the [Polkadot-JS API Documentation](https://polkadot.js.org/api/) and the [oo7 API Documentation](https://paritytech.github.io/oo7/).

Rust

> module functions must return the Result type   
> which allows us to handle errors within our functions.   
> The returned Result is either Ok() for success or Err() for a failure.  
> Throughout this tutorial we will use the question mark operator (?)  
> at the end of functions which return a Result. 
> When calling a function like this, for example 

    my_function()?
    
returns `value`, or `Err(msg)`

The included template.rs stores an u32!

--> made a standalone repo `substrate-package-chainhammer` which provides a

    chainhammer.store_value(somevalue)

and because cleaned and deleted, not much else.

# issues
* [pja#2205](https://github.com/polkadot-js/apps/issues/2205) ANY transaction results in ExtrinsicStatus:: 1010: Invalid Transaction: 0