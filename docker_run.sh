echo off
echo "Building a docker image: (docker build --rm -t sp500 .)"
echo "----------------------------------"
docker build --rm -t sp500 .
echo "----------------------------------"
read -p "Press enter to continue"

echo "Starting the container using the docker image: (docker run -dp 8888:8888 --name=c-sp500 sp500)"
echo "----------------------------------"
docker run -dp 8888:8888 --rm --name=c-sp500 sp500
read -p "Container is running. Press enter to continue"
docker exec c-sp500 jupyter server list
echo "----------------------------------"
echo "Please open click on the link above to open jupiter lab in browser"
echo "----------------------------------"
read -p "Press enter to continue"

echo "----------------------------------"
echo "Stop and delete the container (docker rm -f c-sp500)"
echo "----------------------------------"
docker rm -f c-sp500
echo "----------------------------------"

echo "Delete images (docker image prune and docker image rm sp500)"
read -p "Are you agree to delete those images: sp500? Y/n " a
echo "$a"
if [ $a == "Y" ] || [ $a == "y" ]; then
  docker image prune -f && docker image rm sp500
fi

echo "----------------------------------"
echo "You have got those images:"
docker images
echo "----------------------------------"
echo "-------------END------------------"
