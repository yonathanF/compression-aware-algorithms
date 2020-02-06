# compressions.py

import LZ78
import matplotlib.pyplot as plt
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

def same_index_diff_compression(num_tokens,index_diff):
	result = []
	for i in range(num_tokens):
		index_to_use = max(0,i - index_diff)
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

fig = plt.figure()  # an empty figure with no axes
fig.suptitle('No axes on this figure')  # Add a title so we know which it is
fig, ax_lst = plt.subplots(2, 2)  # a figure with a 2x2 grid of Axes
num_tokens = 1000
num_trials = 1
for i in range(1,num_tokens):
	for j in range(num_trials):
		comp = same_index_diff_compression(num_tokens,i)
		CR = compressionRatio(comp)
		# print(comp)
		# string = decompress(comp)
		# print(string)
		print("index diff:",i,"compression ratio:",CR)