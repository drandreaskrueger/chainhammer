echo sudo netstat
sudo netstat -tulpn | grep ":8545\|:8546\|:8547\|:8548\|:30303\|:21000\|:21001\|:21002\|:21003\|:21004\|:22000\|:22001\|:22002\|:22003\|:22004\|:9000\|:9001\|:9002\|:9003\|:9004\|docker-proxy"

echo
echo typical process names
ps aux | grep -v grep | grep "tps.py\|crux\|geth\|parity\|start.sh"

echo
echo or simply look around with:
echo ps aux
echo

