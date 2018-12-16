echo
echo link checker
echo must be in root folder chainhammer
echo
echo probably best run when piping the results into a file, like this
echo "scripts/link-checker.sh | tee logs/link-checker.log"
echo
read -p "Press enter to continue"
echo

echo
docker run -ti --rm -v $PWD:/mnt:ro dkhamsing/awesome_bot --allow-dupe --allow-redirect --skip-save-results `ls *.md`
echo
cd docs
docker run -ti --rm -v $PWD:/mnt:ro dkhamsing/awesome_bot --allow-dupe --allow-redirect --skip-save-results `ls *.md`
echo
cd ../hammer
docker run -ti --rm -v $PWD:/mnt:ro dkhamsing/awesome_bot --allow-dupe --allow-redirect --skip-save-results `ls *.md`
echo
cd ../logs
docker run -ti --rm -v $PWD:/mnt:ro dkhamsing/awesome_bot --allow-dupe --allow-redirect --skip-save-results `ls *.md`
echo
cd ../networks
docker run -ti --rm -v $PWD:/mnt:ro dkhamsing/awesome_bot --allow-dupe --allow-redirect --skip-save-results `ls *.md`
echo
cd ../reader
docker run -ti --rm -v $PWD:/mnt:ro dkhamsing/awesome_bot --allow-dupe --allow-redirect --skip-save-results `ls *.md`
echo
cd ../results
docker run -ti --rm -v $PWD:/mnt:ro dkhamsing/awesome_bot --allow-dupe --allow-redirect --skip-save-results `ls *.md`
echo
cd ../scripts
docker run -ti --rm -v $PWD:/mnt:ro dkhamsing/awesome_bot --allow-dupe --allow-redirect --skip-save-results `ls *.md`
echo
cd ../tests
docker run -ti --rm -v $PWD:/mnt:ro dkhamsing/awesome_bot --allow-dupe --allow-redirect --skip-save-results `ls *.md`
cd ..
echo 
echo done.
echo


