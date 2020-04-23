# compressions.py
import LZ78
decompress = LZ78.decode
compress = LZ78.encode

# what characters do we choose from when adding a token to a random
# compression?
import string
letters = string.ascii_letters

import random
import math
import numpy as np
# a more obscure piecewise linear fit library
# https://github.com/cjekel/piecewise_linear_fit_py
try:
    import pwlf
except ImportError:
    print("pip install pwlf")
    exit()

def withinTolerance(x, y, tolerance):
    return abs((x / y) - 1) < tolerance

#random compression by num tokens
def random_compression_tokens(compression_ratio, num_tokens=500, tolerance=0.05, reject=False):
    CRToDiff = deriveCRToDiff(num_tokens)
    avgIndexDiff = CRToDiff(compression_ratio)
    chanceToLower = avgIndexDiff % 1
    index_diff = int(avgIndexDiff)
    if(random.random() > chanceToLower):
        index_diff += 1
    comp = same_index_diff_compression(num_tokens, index_diff)
    if(reject):
        while not withinTolerance(compressionRatio(comp), compression_ratio, tolerance):
            comp = same_index_diff_compression(num_tokens, index_diff)
    return comp

#nearest multiple of x above n
def nearest_multiple_above(n,x):
    return ((n//x) + 1)*x

#want the string to be an exact size
#so generate a compression, then cut the string down to size
#then return compression of that
def truncated_compression(compression_ratio, num_tokens, string_size):
    comp = random_compression_tokens(compression_ratio, num_tokens)
    decomp = decompress(comp)
    if(len(decomp)>string_size):
        comp = compress(decomp[:string_size])
    return comp

#gives a compression which decompresses to a specified string size
#with approximately a target compression ratio
def random_compression(compression_ratio, string_size=2000, tolerance=0.05, reject=False):
    num_tokens = nearest_multiple_above(int(round(string_size / compression_ratio)),100)
    comp = truncated_compression(compression_ratio, num_tokens, string_size)
    if(reject):
        while not withinTolerance(compressionRatio(comp), compression_ratio, tolerance):
            comp = truncated_compression(compression_ratio, num_tokens, string_size)
    return comp

#gives a compression with the same back pointer distance in every cell
def same_index_diff_compression(num_tokens, index_diff, index_randomness=1):
    result = []
    for i in range(num_tokens):
        index_to_use = i - index_diff + random.randrange(-index_randomness, index_randomness + 1)
        index_to_use = max(0, min(i, index_to_use))
        result.append((index_to_use, letters[random.randrange(0, len(letters))]))
    return result


def compressionRatio(compression):
    string = decompress(compression)
    newcomp = compress(string)
    return len(string) / len(newcomp)


def generateData(num_tokens=500, index_randomness=1, num_trials=10):
    diffs = []
    CRs = []
    # TODO this outer loop is slow but can be done in parallel or using map
    # syntax
    for i in range(1, num_tokens):
        avg_CR = 0
        for j in range(num_trials):
            comp = same_index_diff_compression(num_tokens, i, index_randomness)
            avg_CR += compressionRatio(comp)
        avg_CR /= num_trials
        diffs.append(i / num_tokens)
        CRs.append(avg_CR)
    return (np.array(diffs), np.array(CRs))


def findPiecewiseFit(data):
    x = data[0]
    y = data[1]
    y = np.reciprocal(y * y)
    piecewiseFit = pwlf.PiecewiseLinFit(x, y)
    res1 = piecewiseFit.fit(3)  # this gets very slow at about 6 line segments
    return piecewiseFit


def piecewiseEvaluate(x, breakpoints, breakpointYs, slopes):
    if(x < breakpoints[0]):
        return (x - breakpoints[0]) * slopes[0] + breakpointYs[0]
    if(x >= breakpoints[-1]):
        return (x - breakpoints[-1]) * slopes[-1] + breakpointYs[-1]
    for i in range(1, len(breakpoints)):
        if(x < breakpoints[i]):
            return (x - breakpoints[i - 1]) * slopes[i - 1] + breakpointYs[i - 1]


def piecewiseInverse(fit):
    for slope in fit.slopes:
        if(slope <= 0):
            print("fit is not strictly increasing, so I can't invert it")
            return
    newBreakpoints = fit.predict(fit.fit_breaks)
    newBreakpointYs = fit.fit_breaks
    newSlopes = np.reciprocal(fit.slopes)

    def invertedFit(x):
        return piecewiseEvaluate(x, newBreakpoints, newBreakpointYs, newSlopes)
    return (invertedFit,newBreakpoints,newBreakpointYs,newSlopes)

#retrieve previous models from file
def listFromString(string):
    badchars = "()[],"
    for ch in badchars:
        string = string.replace(ch,"")
    return list(map(float,string.split()))
def tupleFromString(string):
    badchars = "()[],"
    for ch in badchars:
        string = string.replace(ch,"")
    return tuple(map(int,string.split()))
models_filename = "models.txt"
prevModels = {}
def extractModels():
    with open(models_filename,"r") as models:
        while(True):
            line = models.readline()
            if line == "":
                break
            key = tupleFromString(line)
            num_tokens = key[0]
            print("retrieving model for", num_tokens, "tokens")
            breaks = listFromString(models.readline())
            breakYs = listFromString(models.readline())
            slopes = listFromString(models.readline())
            print(key)
            print(breaks)
            print(breakYs)   
            print(slopes)
            def invertedFit(x):
                return piecewiseEvaluate(x, breaks, breakYs, slopes)
            def result(compression_ratio):
                return invertedFit(1 / (compression_ratio * compression_ratio)) * num_tokens
            prevModels[key] = result
extractModels()

def printToFile(filename, *args):
    with open(filename, "a") as f:
        for arg in args:
            f.write(str(arg)+'\n')

def deriveCRToDiff(num_tokens):
    key = (num_tokens,len(letters))
    if key in prevModels:
        return prevModels[key]
    print("deriving model for", num_tokens, "tokens")
    data = generateData(num_tokens)
    piecewiseFit = findPiecewiseFit(data)
    invertedFit,breaks,breakYs,slopes = piecewiseInverse(piecewiseFit)
    printToFile(models_filename,key,breaks,breakYs,slopes)

    def result(compression_ratio):
        return invertedFit(1 / (compression_ratio * compression_ratio)) * num_tokens
    prevModels[key] = result
    return result

# import sys
# # helper for testing
# def frange(start, stop, step):
#     i = start
#     while i < stop:
#         yield i
#         i += step

# string_size = 500
# num_trials = 30
# if(len(sys.argv) > 1):
#     toks = int(sys.argv[1])
# for CR in frange(2, 10, 0.1):
#     avg_CR = 0
#     for trial in range(num_trials):
#         comp = random_compression_tokens(CR, string_size, reject=False)
#         avg_CR += compressionRatio(comp)
#     avg_CR /= num_trials
#     print("target:", round(CR, 2), "\tactual:", round(avg_CR, 2))
