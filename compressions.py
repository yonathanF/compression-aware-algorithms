# compressions.py

import LZ78
# import matplotlib.pyplot as plt
import random
import string
letters = string.ascii_lowercase


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
		index_to_use = max(0,i - index_diff+random.randrange(-index_randomness,index_randomness+1))
		result.append((index_to_use, letters[random.randrange(0,len(letters))]))
	return result

def random_compression(string_size,num_tokens):
	pass

def random_compression_2(compression_ratio,string_size):
	pass

def decompress(compression):
	return LZ78.decode(compression)

def compressionRatio(compression):
	string = decompress(compression)
	return len(string) / len(compression)

num_tokens = 1000
index_randomness = 1
num_trials = 200
for i in range(1,num_tokens):
	avg_CR = 0
	for j in range(num_trials):
		comp = same_index_diff_compression(num_tokens,i,1)
		avg_CR += compressionRatio(comp)
		# print(comp)
		# string = decompress(comp)
		# print(decompress(comp))
	avg_CR /= num_trials
	print("index diff:",i,"compression ratio:",round(avg_CR,2))