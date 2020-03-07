# substrate subkey command 

As long as the polkascan library is still "read only" we must use `subkey` to sign transactions.

Turns out it has a bug: [pts#5180](https://github.com/paritytech/substrate/issues/5180) see below.

And the `sign-transaction` subcommand is the "missing chapter" in https://substrate.dev/docs/en/ecosystem/subkey#signing-and-verifying-messages

## issues
* [pts#5180](https://github.com/paritytech/substrate/issues/5180) subkey sign-transaction = panicked `Option::unwrap()` on a `None` value
