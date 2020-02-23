import math
import numpy as np
import pandas
import csv

byte_dictionary = {}
total_byte_count = 0
#add up the occurences of each type of byte
with open("bit_list.bin", "rb") as f:
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

print(entropy_return)
