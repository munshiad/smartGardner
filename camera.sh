#!/bin/bash
FSWEB=$(dpkg -l | grep fswebcam)
if [ -z "$FSWEB" ]; then
  sudo apt-get install fswebcam
fi
SIZES=('320x240' '640x480' '1024x768')
F=0
# INDEX= $(($SELECT - 1))
INDEX=0
RES=$(echo ${SIZES[$INDEX]})
FRAMES=1
DELAY=0

while [[ $F < $FRAMES ]]; do
  F=$(($F + 1))
  DIR="camera/"
  IMAGE="image.jpg"
  fswebcam -q -r $RES --no-banner $DIR$IMAGE
  if [[ $DELAY > 0 ]]; then
    sleep $DELAY
  fi
  echo $IMAGE
done
