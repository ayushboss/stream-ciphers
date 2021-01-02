import numpy as np
import pandas as pd
import seaborn as sns
import os
import sys
import matplotlib.pyplot as plt

def analyzeRawData(prng_name):
	pathToCSV = "../cluster_data/sp800_collected_cluster_data_" + str(prng_name) + "_fix2.csv"
	# if not os.path.exists(pathToCSV)
	# 	print('Error: PRNG type does not exist.')
	# 	return
	#still need to standardize the optimal values that aren't 0
	optimal_point = [0, 0, 1029000/2, 0, 0, 0, 0, 0, 0, 7]
	#Standardized version of the optimal point in order to ensure 
	#that all features are equally weighted
	optimal_point_binary = [0,0,0.5,0,0,0,0,0,0,1]

	#123 is DFT since i couldnt find one
	max_list = [1014.3963722332606,1028907,1029000,1050.0,6526.0,123, 24117.125,13068.0,190855.0,7]


	data = pd.read_csv('../cluster_data/sp800_collected_cluster_data_' + str(prng_name) + '_fix2.csv', error_bad_lines=False, engine="python") #reads and parses the data
	df = pd.DataFrame(data)

	testNames = list(df.columns)

	sns.heatmap(df.corr().abs())
	plt.show()

	dfMatrix = df.values.tolist()

	correlationValues = df.corr().abs()
	cv = correlationValues.unstack()

	so = cv.sort_values(kind="quicksort")
	so = np.flip(so)
	print("Sorted correlation:")
	print(so)

	for idx in range(0, len(max_list)):
		tempList = []
		for row in dfMatrix:
			tempList.append(row[idx])
		plt.hist(tempList,100)
		plt.title(testNames[idx])
		plt.show()

def main():
	if len(sys.argv) > 2:
		print("Error: too many arguments.")
		return
	elif len(sys.argv) < 2:
		print("Error: Usage: python3 raw_data_analysis.py prng_name")
		return
	analyzeRawData(sys.argv[1])

if __name__ == '__main__':
	main()



# plot histograms of the raw scores to look at the distribution of scores 
# look at correlations of the raw scores between prng tests (like original)
	# are they testing two linked aspects or orthagonal aspects
#negative correlation 


#on paper, indicate the range of each test rather than scaling and combining
#
#put ranges of each prng on one table and put statistical data 