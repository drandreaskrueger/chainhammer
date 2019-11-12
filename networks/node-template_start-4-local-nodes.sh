node-template --telemetry-url ws://telemetry.polkadot.io:1024  \
              --node-key 0000000000000000000000000000000000000000000000000000000000000001 \
              --validator --chain=local \
	      --alice --name CH_Alice --base-path /tmp/alice > logs/substrate_alice.log 2>&1 &

ALICE=/ip4/127.0.0.1/tcp/30333/p2p/QmRpheLN4JWdAnY7HGJfWFNbfkQCb6tFf4vvA6hgjMZKrR

node-template --telemetry-url ws://telemetry.polkadot.io:1024 \
              --chain=local  --validator --bootnodes $ALICE \
              --bob --name CH_Bob --base-path /tmp/bob --port 30334 > logs/substrate_bob.log 2>&1 &

node-template --telemetry-url ws://telemetry.polkadot.io:1024 \
              --chain=local  --validator --bootnodes $ALICE \
              --charlie --name CH_Charlie --base-path /tmp/charlie --port 30335 > logs/substrate_charlie.log 2>&1 &

node-template --telemetry-url ws://telemetry.polkadot.io:1024 \
              --chain=local  --validator --bootnodes $ALICE \
              --dave --name CH_Dave --base-path /tmp/dave --port 30336 > logs/substrate_dave.log 2>&1 &

echo
echo the 4 nodes should be started now, watch their logs with this:
echo tail -f logs/substrate_alice.log logs/substrate_bob.log logs/substrate_charlie.log logs/substrate_dave.log
