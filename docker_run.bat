echo off
echo Building a docker image: (docker build --rm -t sp500 .)

echo ----------------------------------
docker build --rm -t sp500 .
echo ----------------------------------
set /p a="Image is ready. Press enter to continue"

echo Starting the container using the docker image: (docker run -dp 8888:8888 --name=c-sp500 sp500)
echo ----------------------------------
docker run -dp 8888:8888 --rm --name=c-sp500 sp500

echo wait for running jupyter server
timeout /nobreak /t 15
docker exec c-sp500 jupyter server list
echo ----------------------------------
echo Please open click on the link above to open jupiter lab in browser
echo ----------------------------------

echo After you finish testing, press enter and I will remove container and image(s) from your OS
set /p a="Press enter to continue"

echo ----------------------------------
echo Stop and delete the container (docker rm -f c-sp500)
echo ----------------------------------
docker rm -f c-sp500

echo Delete images (docker image prune and docker image rm sp500)
set /p a="Are you agree to delete those images: sp500? Y/n "
echo %a%
echo ----------------------------------
if /i %a% == "y" docker image prune -f && docker image rm -f sp500

echo ----------------------------------
echo You have got those images:
docker images
echo ----------------------------------
echo -------------END------------------
