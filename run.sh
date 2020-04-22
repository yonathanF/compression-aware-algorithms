#!/bin/bash

gcc -shared -o metrics.so -fPIC metrics.c
# python3 -u heatmap.py
python3 -u heatmap.py | tee data/output.txt

grep "Hamming" data/output.txt >> data/HammingData.txt
grep "LCS" data/output.txt >> data/LCSData.txt
grep "Edit" data/output.txt >> data/EditData.txt