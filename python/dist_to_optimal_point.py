import numpy as np
import pandas as pd

#still need to standardize the optimal values that aren't 0
optimal_point = [1, 1, 0, 0, 1029000/2, 0, 0, 0, 0, 0, 6, 0, 0]

max_list = []

max_data =pd.read_csv('../cluster_data/max.csv', error_bad_lines=False, engine="python")
max_df = pd.DataFrame(max_data)

maxMatrix = max_df.values.tolist()

for row in maxMatrix:
	for cell in row:
		print(cell)
		max_list.append(cell)

print("Max List: " + str(max_list))


data = pd.read_csv('../cluster_data/Philox/Philox_all_cluster_data.csv', error_bad_lines=False, engine="python") #reads and parses the data
df = pd.DataFrame(data)


#Matrix of all rows in our file
dfMatrix = df.values.tolist()

print (type(dfMatrix))

#standardizing measurements
rowIdx = 0
for dfRow,maxRow in zip(dfMatrix, maxMatrix):
	colIdx = 0
	for cellDf, cellMax in zip(dfRow, maxRow):
		maxPossibleTest = cellMax
		standardizedValue = (cellDf)/(maxPossibleTest) #the minimum value for all of the tests is 0 so we don't need to include it in the calculation
		print(str(cellDf) + " standardized to " + str(standardizedValue))
		dfMatrix[rowIdx][colIdx] = standardizedValue
		colIdx+=1
	rowIdx+=1


avgDistance = 0 #represents average distance to our point of optimal "randomness"
numRows = 0

for row in dfMatrix:
	numRows += 1
	tempDistance = 0
	idx = 0
	for cell in row:
		print("cell: " + str(cell) + " " + str(optimal_point[idx]))
		tempDistance += (cell - optimal_point[idx])*(cell - optimal_point[idx])
		idx+=1
	avgDistance += np.sqrt(tempDistance)

avgDistance /= numRows

print("Quality of Philox: " + str(avgDistance))




