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

data_filename = 'data/memo.dat'

def compression_ratio(decompressed):
    return len(decompressed)/len(encode(decompressed))

def raw_data(CRs, num_data_points=100):
    CR1, CR2 = CRs
    print("Running {} and {}".format(CR1, CR2))
    data = np.zeros((num_data_points, len(metrics)+2),dtype=float)
    for i in range(num_data_points):
        S1,S2 = map(decode, map(random_compression, (CR1, CR2)))
        realCR1,realCR2 = tuple(map(compression_ratio, (S1,S2)))
        data[i,0] = realCR1
        data[i,1] = realCR2
        for index, metric in enumerate(metrics):
            metric_score = metrics[metric](S1,S2)
            data[i,index+2] = metric_score
    return data

def flat_map(l):
    result = []
    for thing in l:
        result.extend(thing)
    return result

def make_heatmap(f, min_limit, max_limit, steps=1.0):
    print("Making heatmap with Min {:.3f} and Max {:.3f}".format(
    min_limit, max_limit))
    cr_x = np.arange(min_limit, max_limit, steps)
    cr_y = np.arange(min_limit, max_limit, steps)
    with Pool(10) as p:
        result = np.array(flat_map(p.map(f, itertools.product(cr_x, cr_y))))
    result.tofile(data_filename)
    return result

def plot(data=None):
    if data is not None:
        data = np.fromfile(data_filename, dtype=float)
        num_cols = len(metrics) + 2
        data = data.reshape((len(data)//num_cols,num_cols))
    column_labels = ['CR of String 1', 'CR of String 2']
    for metric in metrics:
        column_labels.append(metric)
    data = pd.DataFrame(data, columns = column_labels)
    sns.set(style="whitegrid")



# def makeHeatmap():
#     result = np.fromfile('memo.dat', dtype=float)
#     result = result.reshape((len(result)//5, 5))
#     result = pd.DataFrame(result,
#                           columns=['Ave CR1', 'Ave CR2', 'STD in Hamming Distance', 'STD in Edit Distance', 'STD in LCS'])
#     sns.set(style="whitegrid")
#     # ax = plt.axes(projection='3d')
#     # ax.scatter(x, y, z, c=z)
#     # ax.set_xlabel('Ave compression ratio of S1')
#     # ax.set_ylabel('Ave compression ratio of S2')
#     # ax.set_zlabel('STD in Metric x')
#     # ax.set_title('Compression ratio vs STD in metric')
#     t = ['STD in Hamming Distance', 'STD in LCS', 'STD in Edit Distance']
#     for i in range(1, 4):
#         plt.subplot(1, 3, i)
#         ax = sns.scatterplot(x='Ave CR1', y='Ave CR2',
#                               hue=t[i-1], size=t[i-1], data=result)
#         ax.set_xlabel('Ave compression ratio of S1')
#         ax.set_ylabel('Ave compression ratio of S2')
#         ax.set_title('Compression ratio vs {}'.format(t[i-1]))
#     # for i in range(1, 4):
#         # fig = plt.figure()
#         # ax = fig.add_subplot(222, projection='3d')
#         # ax = plt.axes(projection='3d')
#         # ax.scatter(result['Ave CR1'], result['Ave CR2'], result[t[i-1]], c=result[t[i-1]])
#         # ax.set_xlabel('Ave compression ratio of S1')
#         # ax.set_ylabel('Ave compression ratio of S2')
#         # ax.set_zlabel(t[i-1])
#         # ax.set_title('Compression ratio vs {}'.format(t[i-1]))
#     plt.show()


plot(make_heatmap(raw_data, 5, 7, 1))
# plot(make_heatmap(raw_data, 5, 20, 1))