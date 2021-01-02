import numpy as np
import pandas as pd
import os
import sys


def getAvgData(prng_name):
	data = pd.read_csv('../cluster_data/sp800_collected_cluster_data_' + str(prng_name) + '_fix2.csv', error_bad_lines=False, engine="python") #reads and parses the data
	df = pd.DataFrame(data)
	dfMatrix = df.values.tolist()

	avgList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(0,len(dfMatrix[0])):
		for j in range(0, len(dfMatrix)):
			avgList[i] = avgList[i] + dfMatrix[j][i]
		avgList[i] = avgList[i]/len(dfMatrix)
	return avgList

def main():
	if len(sys.argv) > 2:
		print("Error: too many arguments.")
		return
	elif len(sys.argv) < 2:
		print("Error: Usage: python3 dist_to_optimal_point.py prng_name")
		return
	avgList = getAvgData(sys.argv[1])
	print(avgList)

if __name__ == '__main__':
	main()