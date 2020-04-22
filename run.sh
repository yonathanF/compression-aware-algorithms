#!/bin/bash

gcc -shared -o metrics.so -fPIC metrics.c

python3 -u heatmap.py | tee -a output.txt