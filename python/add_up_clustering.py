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


data = pd.read_csv('../cluster_data.csv', error_bad_lines=False, engine="python") #reads and parses the data

print(type(data))

n_clusters = 5

df = pd.DataFrame(data)
columns = list(df)
features = []
for column in df:
	epiclist = df[column] # epiclist = values for a certain feature for all iterations
	features.append(epiclist)

#generates a heatmap that we can use to find strongly correlated values
plt.figure(figsize=(12,10))
cor = df.corr()
sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
plt.show()

#attempt add up	

best_features_per_num_of_features = []

features_already_included = []
for r in range(0, len(features)): # r represents the number of features we are adding
	print(len(features_already_included))
	best_features = []
	for i in features_already_included:
		best_features.append(features[i])
	print ("jgh: " + str(best_features) )
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
	best_features.append(features[best_coeff_idx])
	features_already_included.append(best_coeff_idx)
	best_features_per_num_of_features.append(best_features)
	print(len(best_features))

for i in range(0, len(best_features_per_num_of_features)):
	print("Best features for " + str(i + 1) + ": " + str(len(best_features_per_num_of_features[i])) )
