# heatmap.py

from metrics import metrics
from compressions import random_compression
from LZ78 import decode
import matplotlib.pyplot as plt
import numpy as np

def test(CR1, CR2):
    print("\tComparing {} and {}".format(CR1, CR2))
    iters = 1
    results = np.zeros((len(metrics), iters))
    for i in range(iters):
        decompressed = tuple(map(decode, map(random_compression, (CR1, CR2))))
        for index, metric in enumerate(metrics):
            results[index][i] = metrics[metric](decompressed[0],decompressed[1])
    results = np.mean(results, axis=1)
    return {a:b for a,b in zip(metrics,results)}

def frange(start, stop, step=0.1):
    i = start
    while i < stop:
        yield i
        i += step

def makeHeatmap(min_limit, max_limit):
    print("Making heatmap with Min {} and Max {}".format(min_limit, max_limit))
    for i in frange(min_limit, max_limit):
        for j in frange(i, max_limit):
            print(test(i, j))

makeHeatmap(0.1, 2)
