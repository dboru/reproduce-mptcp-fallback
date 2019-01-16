#!/bin/bash


controller="./controllers/controller.py"
observe=1
rest=1

# ryu-manager $controller --observe-links &

ryu-manager $controller &

sleep 2

sudo python mfull-mesh.py

sim=$!

echo 'python script process id: $sim' 

sudo mn -c
