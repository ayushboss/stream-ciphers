import numpy as np
import pandas as pd
import os
import sys

def analyzeDistToOptimalPoint(prng_name):
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


	#Matrix of all rows in our file
	dfMatrix = df.values.tolist()

	standardizedData = []

	for dfRow in dfMatrix:
		newRow = []
		for cellDf, cellMax in zip(dfRow, max_list):
			maxPossibleTest = cellMax
			#print("Cell DF: " + str(cellDf) + ", max: " + str(maxPossibleTest) + ", quotient: " + str(cellDf/maxPossibleTest))

			standardizedValue = (float(cellDf))/(float(maxPossibleTest)) #the minimum value for all of the tests is 0 so we don't need to include it in the calculation
			newRow.append(standardizedValue)
			
		standardizedData.append(newRow)

	avgDistance = 0 #represents average distance to our point of optimal "randomness"

	iteration = 0
	for row in standardizedData:
		iteration+=1
		tempDistance = 0
		idx = 0
		for cell in row:
			#print("-Cell: " + str(cell) + ", " + str(optimal_point_binary[idx]))
			tempDistance += (cell - optimal_point_binary[idx])*(cell - optimal_point_binary[idx])
			# print ("current data: " + str((cell - optimal_point_binary[idx])*(cell - optimal_point_binary[idx])) + ", row data: " + str(np.sqrt(tempDistance)))
			idx+=1
			print (tempDistance)
		#print("row distance: " + str(tempDistance))
		avgDistance += np.sqrt(tempDistance)
		# print(str(iteration) + ": " + str(np.sqrt(tempDistance)) + ", " + str(avgDistance))
		# print(avgDistance)
	avgDistance /= len(standardizedData)

	print("Quality of " + str(prng_name) + ": " + str(avgDistance))

def main():
	if len(sys.argv) > 2:
		print("Error: too many arguments.")
		return
	elif len(sys.argv) < 2:
		print("Error: Usage: python3 dist_to_optimal_point.py prng_name")
		return
	analyzeDistToOptimalPoint(sys.argv[1])

if __name__ == '__main__':
	main()



# plot histograms of the raw scores to look at the distribution of scores 
# look at correlations of the raw scores between prng tests (like original)
	# are they testing two linked aspects or orthagonal aspects
#negative correlation 


#on paper, indicate the range of each test rather than scaling and combining
#
#put ranges of each prng on one table and put statistical data 