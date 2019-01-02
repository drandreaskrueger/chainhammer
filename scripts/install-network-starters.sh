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
rm -rf paritytech_parity-deploy
git clone https://github.com/paritytech/parity-deploy.git paritytech_parity-deploy
echo TODO: Perhaps already patch with chainhammer-optimized parameters?

echo
rm -rf drandreaskrueger_geth-dev
echo javahippie/geth-dev my configured fork drandreaskrueger/geth-dev 
git clone https://github.com/drandreaskrueger/geth-dev.git drandreaskrueger_geth-dev
echo TODO: Perhaps instead clone from upstream and patch with chainhammer-specific parameters?

echo 
echo blk-io/crux
rm -rf blk-io_crux
git clone  https://github.com/blk-io/crux blk-io_crux
cd blk-io_crux
git checkout f39db2345cf9d82e76d3905468e6e5ea1469b09d
cd ..
echo TODO: Perhaps already patch with chainhammer-optimized parameters?

cd ../..

echo
echo
echo