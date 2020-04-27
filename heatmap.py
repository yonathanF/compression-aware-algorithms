# heatmap.py
from os import getcwd
from ctypes import *
import itertools
# from metrics import metrics
from compressions import random_compression
from LZ78 import (decode, encode)
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits import mplot3d
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from multiprocessing import Pool
import seaborn as sns
import pandas as pd

# metrics
# this can't be a separate file because python doesn't know how
# to import a dynamically linked library like this
so_file = getcwd() + "/metrics.so"
cmetrics = CDLL(so_file)


def char_p(s):
    return c_char_p(s.encode())


def LCS(s1, s2):
    return cmetrics.lcs(char_p(s1), char_p(s2), c_int(len(s1)), c_int(len(s2)))


def EditDistance(s1, s2):
    return cmetrics.edit_distance(char_p(s1), char_p(s2), c_int(len(s1)), c_int(len(s2)))


def HammingDistance(s1, s2):
    if len(s1) != len(s2):
        smaller = min(len(s1), len(s2))
        return HammingDistance(s1[:smaller], s2[:smaller])
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

# the Needleman-Wunsch algorithm for Sequence Alignment


def SequenceAlignment(s1, s2):
    pass


def StringReconstruction(s1, s2):
    pass


metrics = {
    "Hamming Distance": HammingDistance,
    # "StringReconstruction": StringReconstruction,
    # "SequenceAlignment": SequenceAlignment,
    "Edit Distance": EditDistance,
    "LCS Length": LCS,
}


def compression_ratio(decompressed):
    return len(decompressed)/len(encode(decompressed))


def test(CRs):
    CR1, CR2 = CRs
    print("Running {} and {}".format(CR1, CR2))
    iters = 100
    results = np.zeros((iters, len(metrics)))
    compression_ratios = np.zeros((iters, 2))
    for i in range(max(2, iters)):
        decompressed = tuple(map(decode, map(random_compression, (CR1, CR2))))
        compression_ratios[i][0], compression_ratios[i][1] = tuple(
            map(compression_ratio, decompressed))
        for index, metric in enumerate(metrics):
            metric_score = metrics[metric](
                decompressed[0], decompressed[1])
            results[i][index] = metric_score

    results = np.mean(results, axis=0)
    compression_ratios = np.mean(compression_ratios, axis=0)

    print("Finished running {} and {}".format(CR1, CR2))
    return np.concatenate((compression_ratios, results))


def renew(min_limit, max_limit, steps=1.0):
    print("Making heatmap with Min {:.3f} and Max {:.3f}".format(
        min_limit, max_limit))
    cr_x = np.arange(min_limit, max_limit, steps)
    cr_y = np.arange(min_limit, max_limit, steps)
    with Pool(10) as p:
        result = np.array(list(p.map(test, itertools.product(cr_x, cr_y))))
        result.tofile('memo.dat')


def makeHeatmap():
    result = np.fromfile('memo.dat', dtype=float)
    result = result.reshape((len(result)//5, 5))
    result = pd.DataFrame(result,
                          columns=['Ave CR1', 'Ave CR2', 'STD in Hamming Distance', 'STD in Edit Distance', 'STD in LCS'])

    sns.set(style="whitegrid")
    # ax = plt.axes(projection='3d')
    # ax.scatter(x, y, z, c=z)
    # ax.set_xlabel('Ave compression ratio of S1')
    # ax.set_ylabel('Ave compression ratio of S2')
    # ax.set_zlabel('STD in Metric x')
    # ax.set_title('Compression ratio vs STD in metric')
    t = ['STD in Hamming Distance', 'STD in LCS', 'STD in Edit Distance']
    for i in range(1, 4):
        plt.subplot(1, 3, i)
        ax = sns.scatterplot(x='Ave CR1', y='Ave CR2',
                              hue=t[i-1], size=t[i-1], data=result)
        ax.set_xlabel('Ave compression ratio of S1')
        ax.set_ylabel('Ave compression ratio of S2')
        ax.set_title('Compression ratio vs {}'.format(t[i-1]))

    # for i in range(1, 4):
        # fig = plt.figure()
        # ax = fig.add_subplot(222, projection='3d')
        # ax = plt.axes(projection='3d')
        # ax.scatter(result['Ave CR1'], result['Ave CR2'], result[t[i-1]], c=result[t[i-1]])
        # ax.set_xlabel('Ave compression ratio of S1')
        # ax.set_ylabel('Ave compression ratio of S2')
        # ax.set_zlabel(t[i-1])
        # ax.set_title('Compression ratio vs {}'.format(t[i-1]))

    plt.show()


renew(5, 20, 1)
makeHeatmap()
