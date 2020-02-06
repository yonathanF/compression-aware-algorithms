# compressions.py

import LZ78
# import matplotlib.pyplot as plt
import random
import string
letters = string.ascii_lowercase

def same_index_compression(num_tokens,index_num):
	result = []
	for i in range(num_tokens):
		index_to_use = index_num
		if(i < index_num):
			index_to_use = i
		result.append((index_to_use, letters[random.randrange(0,len(letters))]))
	return result

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

num_tokens = 100
index_randomness = 0
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