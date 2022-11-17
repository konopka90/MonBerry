#!/bin/bash

while true
do
    for i in {1..255}; do i2cset -y -a 1 0x76 $i $(($RANDOM % 255)); done
done