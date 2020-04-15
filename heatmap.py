# heatmap.py

import metrics
import compressions
import matplotlib.pyplot as plt


def test(CR1, CR2):
    iters = 1000
    for i in range(iters):
            # generate a random compression with CR1
            # generate a random compression with CR2
            # evaluate all metrics on this pair of strings
            # store results
        # store average result in heatmap


def makeHeatmap(min, max):
    for i in range(min, max):
        for j in range(i, max):
            test(i, j)
