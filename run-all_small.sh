if [ -z "$CH_MACHINE" ] ; then 
    echo "You must set an ENV variable, example:"
    echo "export CH_MACHINE=Laptop"
    echo "export CH_MACHINE=t2.micro"
    exit
fi

function chapter {

    # helps for debugging if previous clients does not die quickly enough
    # sudo scripts/netstat_port8545.sh

    echo 
    echo
    echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    echo @@@ $1
    echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
}  

# exit when any command fails
set -e
# keep track of the last executed command
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
# echo an error message before exiting
trap 'echo; echo "\"${last_command}\" command filed with exit code $?."' EXIT
#


chapter "TEST: runs on ALL networks, but SMALL number of transactions"
echo
echo machine name: $CH_MACHINE
echo 
if [ "$CH_QUORUM" = true ]; then
    echo You want me to also run Quorum which needs more RAM.
    echo Think twice, this would not work on a t2.micro machine.
    echo Better keep an eye on your RAM, with
    echo 'watch -n 5 "free -m"'
else
    echo Skipping Quorum, good on small machines, if you do want it, set CH_QUORUM=true
fi

echo
sleep 1
echo


chapter "$CH_MACHINE-TestRPC"
CH_TXS=400 CH_THREADING="sequential" ./run.sh "$CH_MACHINE-TestRPC" testrpc



chapter "$CH_MACHINE-Geth"
CH_TXS=3000 CH_THREADING="threaded2 20" ./run.sh "$CH_MACHINE-Geth" geth-clique




chapter "$CH_MACHINE-Quorum"

if [ "$CH_QUORUM" = true ]; then
    networks/quorum-configure.sh
    CH_TXS=4000 CH_THREADING="threaded2 20" ./run.sh "$CH_MACHINE-Quorum" quorum
else
    echo
    echo Skipping Quorum, see very beginning of output of this script.
    echo
fi


chapter "$CH_MACHINE-Parity-instantseal"
PARITY_VERSION=v2.2.3
networks/parity-configure-instantseal.sh $PARITY_VERSION
# would like to run multithreaded too but then parity stops working
# see issue github.com/paritytech/parity-ethereum/issues/9582
# so instead of multithreaded sending:
# TXS=1000 THREADING="threaded2 20" ./run.sh $CH_MACHINE-Parity-instantseal parity
# I must use non-threaded sending:
CH_TXS=2000 CH_THREADING="sequential" ./run.sh "$CH_MACHINE-Parity-instantseal" parity




chapter "$CH_MACHINE-Parity-aura"
networks/parity-configure-aura.sh $PARITY_VERSION
CH_TXS=2000 CH_THREADING="sequential" ./run.sh "$CH_MACHINE-Parity-aura" parity




chapter "run-all_....sh composite script ending here"
echo see folder results/runs/
echo

# switch off the trap
set +e
trap '' EXIT
