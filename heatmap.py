# heatmap.py
import itertools
from metrics import metrics
from compressions import random_compression
from LZ78 import (decode, encode)
import matplotlib.pyplot as plt
import numpy as np


def compression_ratio(decompressed):
    return len(encode(decompressed))/len(decompressed)


def test(CRs):
    CR1, CR2 = CRs
    iters = 1
    results = np.zeros((iters, len(metrics)))
    compression_ratios = np.zeros((iters, 2))
    for i in range(iters):
        decompressed = tuple(map(decode, map(random_compression, (CR1, CR2))))
        compression_ratios[i][0], compression_ratios[i][1] = tuple(
            map(compression_ratio, decompressed))
        for index, metric in enumerate(metrics):
            results[i][index] = metrics[metric](
                decompressed[0], decompressed[1])

    results = np.var(results, axis=0)
    compression_ratios = np.mean(compression_ratios, axis=0)
    return np.concatenate((compression_ratios, results))


def makeHeatmap(min_limit, max_limit):
    print("Making heatmap with Min {} and Max {}".format(min_limit, max_limit))
    size = ((max_limit-min_limit)//0.5)+1
    steps = 0.5
    cr_x = np.arange(min_limit, max_limit, steps)
    cr_y = np.arange(min_limit, max_limit, steps)
    result = map(test, itertools.product(cr_x, cr_y))
    print(np.array(list(result)))


makeHeatmap(0.1, 2)
