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

import numpy as np
# a more obscure piecewise linear fit library
# https://github.com/cjekel/piecewise_linear_fit_py
try:
    import pwlf
except ImportError:
    print("pip install pwlf")
    exit()



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

def generateData(num_tokens=500,index_randomness=1, num_trials=10):
    diffs = []
    CRs = []
    for i in range(1,num_tokens):
      avg_CR = 0
      for j in range(num_trials):
          comp = same_index_diff_compression(num_tokens,i,index_randomness)
          avg_CR += compressionRatio(comp)
      avg_CR /= num_trials
      diffs.append(i/num_tokens)
      CRs.append(avg_CR)
    return (np.array(diffs), np.array(CRs))

def findFit(data):
    x = data[0]
    y = data[1]
    y = np.reciprocal(y*y)
    piecewiseFit = pwlf.PiecewiseLinFit(x,y)
    res1 = piecewiseFit.fit(3)
    return piecewiseFit

num_tokens = 500
if(len(sys.argv) > 1):
    num_tokens = int(sys.argv[1])
print("generating data")
data = generateData(num_tokens)
print("finished generating data")
x = data[0]
y = data[1]
y = np.reciprocal(y*y)
plt.plot(x,y,'o')
plt.ylabel('Average Compression Ratio')
plt.xlabel('Index Diff / Num Tokens')
print("fitting data")
piecewiseFit = findFit(data)
print("finished fitting data")
xd = np.linspace(0, 1, num_tokens*2)
yd = piecewiseFit.predict(xd)
plt.plot(xd,yd)
print("showing plot")
plt.show()