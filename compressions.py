# compressions.py

import LZ78
decompress = LZ78.decode
recompress = LZ78.encode

import matplotlib.pyplot as plt
import random
import math
# from piecewise.regressor import piecewise

import string
letters = string.ascii_letters


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

# for i in range(0,10):
# 	for j in range(100):
# 		print(decompress(same_index_diff_compression(30,5,i)))

num_tokens = 500
index_randomness = 3
num_trials = 10
diffs = []
CRs = []
for i in range(1,num_tokens):
	avg_CR = 0
	for j in range(num_trials):
		comp = same_index_diff_compression(num_tokens,i,index_randomness)
		avg_CR += compressionRatio(comp)
		# print(compressionRatio(comp))
		# string = decompress(comp)
		# print(decompress(comp))
	avg_CR /= num_trials
	diffs.append(i)
	pt = math.pow(avg_CR,-2)
	CRs.append(pt)
	print("index diff:",i,"         compression ratio:",round(pt,2))
plt.scatter(diffs,CRs)
# model = piecewise(diffs,CRs)
plt.ylabel('Average Compression Ratio')
plt.xlabel('Index Diff')
plt.show()