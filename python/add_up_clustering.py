import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import csv

data = pd.read_csv('cluster_data.csv', error_bad_lines=False, engine="python") #reads and parses the data

print(type(data))

n_clusters = 16

df = pd.DataFrame(data)
columns = list(df)
features = []
for column in df:
	epiclist = df[column] # epiclist = values for a certain feature for all iterations
	features.append(epiclist)

#attempt add up	

best_features = []
features_already_included = []
for r in range(0, len(features)): # r represents the number of features we are adding
	best_coeff = 0
	best_coeff_idx = 0
	for d in range(0, len(features)):

		if (d in features_already_included):
			continue

		feature = features[d].copy() # returns the exact feature that we are looking at rn
		best_features.append(features[d])
		clusterer = KMeans(n_clusters=n_clusters, random_state=10)
		
		best_features_df = pd.DataFrame(best_features)
		best_features_df_trans = best_features_df.transpose()
		print(len(best_features_df_trans))

		cluster_labels = clusterer.fit_predict(best_features_df_trans)
		silhouette_avg = silhouette_score(best_features_df_trans, cluster_labels)
		if (silhouette_avg > best_coeff):
			best_coeff_idx = d
			best_coeff = silhouette_avg
		print("Sillhouette score for feature " + str(d) + " is " + str(silhouette_avg))
		del best_features[-1]
	print("yeet: " + str(len(best_features)))
	best_features.append(features[best_coeff_idx])
	features_already_included.append(best_coeff_idx)

print("The List of Best Features is:\n" + str(best_features))


