#!/bin/bash

gcc -g -o socketcanDecodeSignal main.c datenbasis.c processFrame.c lib.c
echo "gcc -g -o socketcanDecodeSignal main.c datenbasis.c processFrame.c lib.c"
echo "Install complete"
