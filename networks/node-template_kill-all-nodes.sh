echo "Killing anything named 'node-template'"
ps aux | grep node-template | grep -v grep | awk '{ print $2 }' | xargs kill 2> /dev/null || echo was not running anyways
sleep 1

echo
echo "Is any such process still running? Then kill manually with 'kill -9 PID'."
echo "ps aux | grep node-template"
ps aux | grep node-template | grep -v grep 

echo 
echo Check these logs, they should be stopped now:
echo tail -f logs/substrate_alice.log logs/substrate_bob.log logs/substrate_charlie.log logs/substrate_dave.log
