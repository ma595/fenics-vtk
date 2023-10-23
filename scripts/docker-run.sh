
if [ $1 == "Run" ] 
then
  echo "creating a docker container"
  sudo docker run -ti --mount type=bind,source=/home/ubuntu/,target=/root/ dolfinx/dev-env:current /bin/bash
fi
