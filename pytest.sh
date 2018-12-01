# BOTH testrpc-py AND pytest must be run in the virtualenv!
source env/py3eth/bin/activate

# py.test needs the unbuffer command to preserve colors
# testrpc needs the unbuffer command to redirect, otherwise log file is empty
# sudo apt-get install expect-dev

# start testrpc, an ethereum simulator, redirect stout/err to file
unbuffer testrpc-py &> tests/logs/testrpc-py.log &

PID=$!
echo testrpc-py started in background, logging into tests/logs/
echo you can watch it with tail -f tests/logs/testrpc-py.log
echo kill it with: kill $PID

# start tests, colored output to screen AND to file
unbuffer py.test -v | tee tests/logs/py.test.log 

echo
echo done.
echo killing the background testrpc-py now:
kill $PID

echo should be gone now:
ps aux | grep testrpc-py | grep -v grep
echo
echo see tests/logs/ for the log files of this test
echo cat tests/logs/*
echo
