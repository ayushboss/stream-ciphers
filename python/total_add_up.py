import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import csv
import seaborn as sns
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
from sklearn.linear_model import RidgeCV, LassoCV, Ridge, Lasso
import sys
import os
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from isodata import find_clusters

data = pd.read_csv('../cluster_datapy.csv', error_bad_lines=False, engine="python") #reads and parses the data

print(type(data))

n_clusters = 5

labels = ["Entropy", "Compression Ratio", "Monobit", "Frequency Within Block", "Runs",
            "Longest Runs in Ones", "Binary Matrix Rank", "DFT", 
            "Non-Overlapping Template", "Overlapping Template", "Maurer's Universal", 
            "Linear Complexity"]
correlating_labels=["Entropy", "Compression Ratio", "Monobit", "Frequency Within Block", "Runs",
            "Longest Runs in Ones", "Binary Matrix Rank", "DFT", 
            "Non-Overlapping Template", "Overlapping Template", "Maurer's Universal", 
            "Linear Complexity"]
df = pd.DataFrame(data)
columns = list(df)
features = []
for column in df:
	epiclist = df[column] # epiclist = values for a certain feature for all iterations
	features.append(epiclist)

#generates a heatmap that we can use to find strongly correlated values
plt.figure(figsize=(12,10))
cor = df.corr(method='pearson')
sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
plt.show()

df.drop(df.index[0])

correlations = {}

for i in range(0, len(labels)):
	label = labels[i]
	cor_target = abs(cor[label])
	relevant_features = cor_target[cor_target>0.15]
	correlations[correlating_labels[i]] = relevant_features
	
#attempt add up	

best_features_per_num_of_features = []
best_coeff_per_num_of_features = []

features_already_included = []

features_already_included_hashing = [False] * len(features)

for r in range(0, len(features)): # r represents the number of features we are adding
	best_features = []

	for i in range(0,len(features_already_included_hashing)):
		if (features_already_included_hashing[i] == True):
			best_features.append(features[i])

	best_coeff = 0
	best_coeff_idx = 0
	for d in range(0, len(features)):
		if (features_already_included_hashing[d] == True):
			continue

		feature = features[d].copy() # returns the exact feature that we are looking at rn
		best_features.append(features[d])
		clusterer = KMeans(n_clusters=n_clusters, random_state=10)
		
		#print (features)

		best_features_df = pd.DataFrame(best_features)
		best_features_df_trans = best_features_df.transpose() #transpose to get everything in terms of trial number rather than test

		cluster_labels = clusterer.fit_predict(best_features_df_trans)
		silhouette_avg = silhouette_score(best_features_df_trans, cluster_labels)
		if (silhouette_avg > best_coeff):
			best_coeff_idx = d
			best_coeff = silhouette_avg
		print("Sillhouette score for feature " + str(d) + " is " + str(silhouette_avg))
		del best_features[-1]

	best_features.append(features[best_coeff_idx])
	features_already_included.append(best_coeff_idx)
	features_already_included_hashing[best_coeff_idx] = True
	best_features_per_num_of_features.append(best_features)
	best_coeff_per_num_of_features.append(best_coeff)

for i in range(0, len(best_features_per_num_of_features)):
	print("_____________________ Best features for " + str(i + 1) + ":  _____________________")
	for x in range(0, len(best_features_per_num_of_features[i])):
		print(best_features_per_num_of_features[i][x].name)
