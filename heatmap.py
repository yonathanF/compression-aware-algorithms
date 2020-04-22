# heatmap.py
import itertools
from metrics import metrics
from compressions import random_compression
from LZ78 import (decode, encode)
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import pickle
from multiprocessing import Pool

def compression_ratio(decompressed):
    return len(encode(decompressed))/len(decompressed)


def test(CRs):
    CR1, CR2 = CRs
    print("    {}, {}".format(CR1,CR2))
    iters = 10
    results = np.zeros((iters, len(metrics)))
    compression_ratios = np.zeros((iters, 2))
    for i in range(max(2, iters)):
        decompressed = tuple(map(decode, map(random_compression, (CR1, CR2))))
        compression_ratios[i][0], compression_ratios[i][1] = tuple(
            map(compression_ratio, decompressed))
        for index, metric in enumerate(metrics):
            metric_score = metrics[metric](
                decompressed[0], decompressed[1])
            print("        {}: {}".format(metric,metric_score))
            results[i][index] = metric_score

    results = np.var(results, axis=0)
    compression_ratios = np.mean(compression_ratios, axis=0)
    return np.concatenate((compression_ratios, results))


def renew(min_limit, max_limit):
    print("Making heatmap with Min {} and Max {}".format(min_limit, max_limit))
    steps = 0.1
    cr_x = np.arange(min_limit, max_limit, steps)
    cr_y = np.arange(min_limit, max_limit, steps)
    with Pool(5) as p:
        result = np.array(list(p.map(test, itertools.product(cr_x, cr_y))))
        result.tofile('memo.dat')


def makeHeatmap():
    result = np.fromfile('memo.dat', dtype=float)
    result = result.reshape((len(result)//5, 5))
    # print(result)
    # TODO avoid duplicates
    ax = plt.axes(projection='3d')
    ax.scatter(result[:, 0], result[:, 1], result[:, 3])
    plt.show()


# renew(0.1, 2)
makeHeatmap()
