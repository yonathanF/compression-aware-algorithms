# heatmap.py

from metrics import metrics
from compressions import random_compression
from LZ78 import decode
import matplotlib.pyplot as plt
import numpy as np

def test(CR1, CR2):
    iters = 10
    results = np.zeros((len(metrics), iters))
    for i in range(iters):
        decompressed = tuple(map(decode, map(random_compression, (CR1, CR2))))
        for index, metric in enumerate(metrics):
            results[index][i] = metrics[metric](decompressed[0],decompressed[1])
    results = np.mean(results, axis=1)
    return {a:b for a,b in zip(metrics,results)}

def makeHeatmap(min_limit, max_limit):
    for i in range(min_limit, max_limit):
        for j in range(i, max_limit):
            print("Running {} and {}".format(i, j))
            print(test(i, j))

makeHeatmap(1, 10)
