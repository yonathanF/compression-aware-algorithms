# compressions.py

import LZ78
decompress = LZ78.decode
recompress = LZ78.encode

import matplotlib.pyplot as plt
import random
import math

#what characters do we choose from when adding a token to a random compression? 
import string
letters = string.ascii_letters

#cmd line args
import sys

# 2-part linear piecewise from here:
# https://stackoverflow.com/questions/46218934/piecewise-linear-fit-with-n-breakpoints
from scipy import optimize
import numpy as np
def linear(k,x0,y0):
    return lambda x:k*x + y0-k*x0
def piecewise_linear(x, x0, y0, k1, k2):
    return np.piecewise(x, [x < x0, x >= x0], [linear(k1,x0,y0), linear(k2,x0,y0)])
def piecewise_linear_three(x, x0, y0, x1, y1, k1, k2, k3):
    return np.piecewise(x, [x < x0, np.logical_and(x >= x0, x < x1), x >= x1], [linear(k1,x0,y0), linear(k2,x0,y0), linear(k3,x1,y1)])
#example use
# x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ,11, 12, 13, 14, 15], dtype=float)
# y = np.array([5, 7, 9, 11, 13, 15, 28.92, 42.81, 56.7, 70.59, 84.47, 98.36, 112.25, 126.14, 140.03])
# p , e = optimize.curve_fit(piecewise_linear, x, y)
# xd = np.linspace(0, 15, 100)
# plt.plot(x, y, "o")
# plt.plot(xd, piecewise_linear(xd, *p))
# plt.show()

# a more obscure piecewise linear fit library
# https://github.com/cjekel/piecewise_linear_fit_py
import pwlf




"""
I am using this to measure the relationship between
average index diff (meaning the number of tokens back a given token's index reaches)
and compression ratio.

You can also supply an amount to perturb the indices by so that you sample a larger range of strings.

After making some plots, I will derive the inverse 
of this relationship so that we have the mapping of
compression ratio |----> average index diff to use
"""
def same_index_diff_compression(num_tokens,index_diff,index_randomness):
    result = []
    for i in range(num_tokens):
        index_to_use = i - index_diff+random.randrange(-index_randomness,index_randomness+1)
        index_to_use = max(0,index_to_use)
        index_to_use = min(i,index_to_use)
        result.append((index_to_use, letters[random.randrange(0,len(letters))]))
    return result

def random_compression(string_size,num_tokens):
    pass

def random_compression_2(compression_ratio,string_size):
    pass

def compressionRatioRatio(compression):
    string = decompress(compression)
    newcomp = recompress(string)
    return len(compression) / len(newcomp)

def compressionRatio(compression):
    string = decompress(compression)
    newcomp = recompress(string)
    return len(string) / len(newcomp)

def findFit(num_tokens=500, index_randomness=1, num_trials=10):
    #something horrible I'm doing to tell findFit to keep trying new data until fitting succeeds
    import warnings
    warnings.filterwarnings("error")

    foundFit = False
    params = None
    roundNum = 0
    while not foundFit:
        print("round",roundNum)
        roundNum += 1
        diffs = []
        CRs = []
        for i in range(1,num_tokens):
          avg_CR = 0
          for j in range(num_trials):
              comp = same_index_diff_compression(num_tokens,i,index_randomness)
              avg_CR += compressionRatio(comp)
          avg_CR /= num_trials
          diffs.append(i/num_tokens)
          pt = math.pow(avg_CR,-2)
          # pt = avg_CR
          CRs.append(pt)
          # print("index diff:",i,"         compression ratio:",round(pt,2))
        diffs = np.array(diffs)
        CRs = np.array(CRs)
        piecewiseFit = pwlf.PiecewiseLinFit(diffs, CRs)
        res1 = piecewiseFit.fit(3, disp=True)
        # try:
            # params , err = optimize.curve_fit(piecewise_linear, diffs, CRs)
        # except optimize.OptimizeWarning:
            # continue
        foundFit = True
        plt.plot(diffs,CRs,'o')
        plt.ylabel('Average Compression Ratio')
        plt.xlabel('Index Diff / Num Tokens')
        xd = np.linspace(0, 1, num_tokens*2)
        yd = piecewiseFit.predict(xd)
        plt.plot(xd,yd)
        plt.show()
    return params

num_tokens = 500
if(len(sys.argv) > 1):
    num_tokens = int(sys.argv[1])
p = findFit(num_tokens)
print("params: ",p)
xd = np.linspace(0, 1, num_tokens*2)
plt.plot(xd, piecewise_linear(xd, *p))
plt.show()