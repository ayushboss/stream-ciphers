import math
import csv

r = csv.reader(open('cluster_data/sp800_collected_cluster_data_MT.csv'))

csvChart = list(r)

for idx in range(1, len(csvChart)):
	print(idx)
	print(type(csvChart[idx][2]))
	print("Old Monobit Value: " + str(csvChart[idx][2]) + ", New Monobit Value: " + str(float(csvChart[idx][2]) * math.sqrt(2)))
	csvChart[idx][2] = float(csvChart[idx][2]) * math.sqrt(2)

writer = csv.writer(open('cluster_data/sp800_collected_cluster_data_MT.csv', 'w'))
writer.writerows(csvChart)
