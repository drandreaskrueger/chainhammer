echo
echo link checker
echo must be in root folder chainhammer
echo
echo probably best run when piping the results into a file, like this
echo "scripts/link-checker.sh | tee logs/link-checker.log"
echo
read -p "Press enter to continue"
echo

# this is the relative url, decide here which branch to check:
BURL="https://github.com/drandreaskrueger/chainhammer/blob/master/"
BURL="https://github.com/drandreaskrueger/chainhammer/tree/reorg/"

# for putting the command together:
BASE1="docker run -ti --rm -v "
BASE2=":/mnt:ro dkhamsing/awesome_bot --allow-dupe --allow-redirect --skip-save-results --base-url "

FOLDER=""
echo; echo root folder of repo:
CMD=$BASE1$(pwd)$BASE2$BURL$FOLDER" *.md" 
echo $CMD; echo
$CMD


FOLDERS="docs/ hammer/ logs/ networks/ reader/ results/ scripts/ tests/"

for FOLDER in $FOLDERS; do
    echo; echo $FOLDER
    cd $FOLDER
    CMD=$BASE1$(pwd)$BASE2"--base-url "$BURL$FOLDER" *.md"  
    echo $CMD; echo
    $CMD
    cd ..
done

echo 
echo done.
echo
