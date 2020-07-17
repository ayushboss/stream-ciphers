import numpy as np
import pandas as pd
import seaborn as sns
import os
import sys
import matplotlib.pyplot as plt

def analyzeStandardDeviation(prng_name):
	pathToCSV = "../cluster_data/sp800_collected_cluster_data_" + str(prng_name) + "_fix2.csv"
	# if not os.path.exists(pathToCSV)
	# 	print('Error: PRNG type does not exist.')
	# 	return
	#still need to standardize the optimal values that aren't 0
	optimal_point = [0, 0, 1029000/2, 0, 0, 0, 0, 0, 7]
	#Standardized version of the optimal point in order to ensure 
	#that all features are equally weighted
	optimal_point_binary = [0,0,0.5,0,0,0,0,0,1]

	max_list = [1014.3963722332606,1028907,1029000,1050.0,6526.0,24117.125,13068.0,190855.0,7]


	data = pd.read_csv('../cluster_data/sp800_collected_cluster_data_' + str(prng_name) + '_fix2.csv', error_bad_lines=False, engine="python") #reads and parses the data
	df = pd.DataFrame(data)

	testNames = list(df.columns)

	dfMatrix = df.values.tolist()
	
	standardDeviation = []

	for idx in range(0, len(max_list)):
		tempList = []
		for row in dfMatrix:
			tempList.append(row[idx])
		standDevCurrentRow = np.std(tempList)
		standardDeviation.append(standDevCurrentRow)

	print(standardDeviation)

def main():
	if len(sys.argv) > 2:
		print("Error: too many arguments.")
		return
	elif len(sys.argv) < 2:
		print("Error: Usage: python3 raw_data_analysis.py prng_name")
		return
	analyzeStandardDeviation(sys.argv[1])

if __name__ == '__main__':
	main()

