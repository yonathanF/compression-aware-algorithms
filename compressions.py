# compressions.py

import LZ78
decompress = LZ78.decode
compress = LZ78.encode

#what characters do we choose from when adding a token to a random compression? 
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

def withinTolerance(x,y,tolerance):
    return abs((x/y) - 1) < tolerance

def random_string(num_chars):
    result = ''
    for i in range(num_chars):
        result += letters[random.randrange(0,len(letters))]
    return result

def random_compression(compression_ratio,num_tokens=500, tolerance = 0.05, reject = False):
    CRToDiff = deriveCRToDiff(num_tokens)
    avgIndexDiff = CRToDiff(compression_ratio)
    chanceToLower = avgIndexDiff % 1
    index_diff = int(avgIndexDiff)
    if(random.random() > chanceToLower):
        index_diff += 1
    comp = same_index_diff_compression(num_tokens,index_diff)
    if(reject):
        while not withinTolerance(compressionRatio(comp), compression_ratio, tolerance):
            comp = same_index_diff_compression(num_tokens,index_diff)
    return comp


def random_compression_2(compression_ratio,string_size=2500, tolerance = 0.05, reject = True):
    num_tokens = int(round(string_size / compression_ratio))
    return random_compression(compression_ratio,num_tokens, tolerance, reject)

def same_index_diff_compression(num_tokens,index_diff,index_randomness=1):
    result = []
    for i in range(num_tokens):
        index_to_use = i - index_diff+random.randrange(-index_randomness,index_randomness+1)
        index_to_use = max(0,min(i,index_to_use))
        result.append((index_to_use, letters[random.randrange(0,len(letters))]))
    return result

def compressionRatio(compression):
    string = decompress(compression)
    newcomp = compress(string)
    return len(string) / len(newcomp)

def generateData(num_tokens=500,index_randomness=1, num_trials=10):
    diffs = []
    CRs = []
    #TODO this outer loop is slow but can be done in parallel or using map syntax
    for i in range(1,num_tokens):
        avg_CR = 0
        for j in range(num_trials):
            comp = same_index_diff_compression(num_tokens,i,index_randomness)
            avg_CR += compressionRatio(comp)
        avg_CR /= num_trials
        diffs.append(i/num_tokens)
        CRs.append(avg_CR)
    return (np.array(diffs), np.array(CRs))

def findPiecewiseFit(data):
    x = data[0]
    y = data[1]
    y = np.reciprocal(y*y)
    piecewiseFit = pwlf.PiecewiseLinFit(x,y)
    res1 = piecewiseFit.fit(3) #this gets very slow at about 6 line segments
    return piecewiseFit

def piecewiseEvaluate(x,breakpoints,breakpointYs,slopes):
    if(x < breakpoints[0]):
        return (x-breakpoints[0])*slopes[0] + breakpointYs[0]
    if(x >= breakpoints[-1]):
        return (x-breakpoints[-1])*slopes[-1] + breakpointYs[-1]
    for i in range(1,len(breakpoints)):
        if(x < breakpoints[i]):
            return (x-breakpoints[i-1])*slopes[i-1] + breakpointYs[i-1]

def piecewiseInverse(fit):
    for slope in fit.slopes:
        if(slope <= 0):
            print("fit is not strictly increasing, so I can't invert it")
            return
    newBreakpoints = fit.predict(fit.fit_breaks)
    newBreakpointYs = fit.fit_breaks
    newSlopes = np.reciprocal(fit.slopes)
    def invertedFit(x):
        return piecewiseEvaluate(x,newBreakpoints,newBreakpointYs,newSlopes)
    return invertedFit

#TODO: memoize to a file so that models are preserved between runs
prevModels = {} #please copy this line with the function
def deriveCRToDiff(num_tokens):
    if(num_tokens in prevModels):
        return prevModels[num_tokens]
    print("deriving model for",num_tokens,"tokens")
    print("    generating data")
    data = generateData(num_tokens)
    print("    generated data")
    print("    fitting data")
    piecewiseFit = findPiecewiseFit(data)
    print("    fitted data")
    invertedFit = piecewiseInverse(piecewiseFit)
    def result(compression_ratio):
        return invertedFit(1/(compression_ratio*compression_ratio))*num_tokens
    prevModels[num_tokens] = result
    return result

# import sys

# #helper for testing
# def frange(start, stop, step):
#     i = start
#     while i < stop:
#         yield i
#         i += step

# toks = 500
# num_trials = 10
# if(len(sys.argv)>1):
#     toks = int(sys.argv[1])
# for CR in frange(5,30,0.5):
#     avg_CR = 0
#     for trial in range(num_trials):
#         comp = random_compression(CR,toks,reject=True)
#         avg_CR += compressionRatio(comp)
#     avg_CR /= num_trials
#     print("target:",round(CR,2),"\tactual:",round(avg_CR,2))