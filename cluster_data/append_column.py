import pandas as pd
import csv
csv_input = pd.read_csv('sp800_collected_cluster_data_threefry_2.csv')
maurersUniversal = []

with open('maurers_data/threefry.csv', 'r') as file:
	reader = csv.reader(file)
	for row in reader:
		maurersUniversal.append(row[0])

csv_input['Maurers'] = maurersUniversal
csv_input.to_csv('sp800_collected_cluster_data_threefry_3.csv', index=False)