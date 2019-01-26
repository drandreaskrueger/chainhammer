FOLDER=./networks/repos/
echo 
echo network starters
echo will be installed into $FOLDER
echo below here
echo $(pwd)
echo
echo careful - whatever was in those subfolders will be gone after this!
read -p "Press enter to continue"

mkdir -p $FOLDER
cd $FOLDER

echo 
echo paritytech/parity-deploy
echo need sudo to remove parity-deploy folder, sorry their decision not mine:
sudo rm -rf paritytech_parity-deploy
git clone https://github.com/paritytech/parity-deploy.git paritytech_parity-deploy
cd paritytech_parity-deploy
git checkout 1a6afd17ac75bdf6c9e9fefa1d3af13748dd9cfa
cd ..

echo
rm -rf drandreaskrueger_geth-dev
echo javahippie/geth-dev my configured fork drandreaskrueger/geth-dev 
git clone https://github.com/drandreaskrueger/geth-dev.git drandreaskrueger_geth-dev
cd drandreaskrueger_geth-dev
echo TODO: Perhaps instead clone from upstream and patch with chainhammer-specific parameters?
cd ..

echo 
echo blk-io/crux
rm -rf blk-io_crux
git clone  https://github.com/blk-io/crux blk-io_crux
cd blk-io_crux
git checkout eeb63a91b7eda0180c8686f819c0dd29c0bc4d46
cd ..


cd ../..

echo
echo
echo