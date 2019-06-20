if [ $# -eq 0 ]
  then
    SIZE=1000
else
    SIZE=$1
fi

echo

free -m

echo
echo creating swap file of size $SIZE
echo
echo do you want that? If not, press Ctrl-C
read -p "Press enter to continue"
echo

SWAPFILE=/swapfile && sudo swapoff -a && sudo dd if=/dev/zero of=$SWAPFILE bs=1M count=$SIZE && sudo chmod 600 $SWAPFILE && sudo mkswap $SWAPFILE && echo $SWAPFILE none swap defaults 0 0 | sudo tee -a /etc/fstab && sudo swapon -a && free -m


