import math
import numpy as np
import pandas
import csv

def get_byte_entropy_bits_func(iteration):
	byte_dictionary = {}
	total_byte_count = 0
	#add up the occurences of each type of byte
	with open("bin_files/bit_list_" + str(iteration) + ".bin", "rb") as f:
		byte = f.read(1)
		while byte:
			byte = f.read(1)
			if not byte in byte_dictionary:
				byte_dictionary[str(byte)] = 1
			else:
				byte_dictionary[str(byte)] += 1
			total_byte_count += 1


	entropy_return = 0.0

	#calculate the entropy
	for x in byte_dictionary.values():
		ratio = ((float(x))/total_byte_count)
		entropy_return += float(ratio) * math.log(ratio)

	entropy_return = entropy_return * -1.0
	return entropy_return
