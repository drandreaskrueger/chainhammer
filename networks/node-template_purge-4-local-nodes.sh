
echo Be aware this might cause problems if nodes are still running.
echo
node-template purge-chain -y --chain=local --base-path /tmp/alice
node-template purge-chain -y --chain=local --base-path /tmp/bob
node-template purge-chain -y --chain=local --base-path /tmp/charlie
node-template purge-chain -y --chain=local --base-path /tmp/dave

