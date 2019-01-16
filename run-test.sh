#!/bin/bash

controller="./controllers/controller.py"
observe=1
rest=1

# ryu-manager $controller --observe-links &

ryu-manager $controller &

sleep 2

sudo python mfull-mesh.py --subflows $1 --pathmanger $2

sim=$!

echo $sim 

sudo mn -c
