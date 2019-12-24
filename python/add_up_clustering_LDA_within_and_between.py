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
from scipy import stats
import pingouin as pg
import sys
import os
import clusteringscoring
from scipy.spatial import distance
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from isodata import find_clusters

def k_mean_distance(data, cx, cy, i_centroid, cluster_labels):
        distances = [np.sqrt((x-cx)**2+(y-cy)**2) for (x, y) in data[cluster_labels == i_centroid]]
        return distances

data = pd.read_csv('../cluster_data/cluster_data_xoroshiro.csv', error_bad_lines=False, engine="python") #reads and parses the data

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

print("checkpoint")
print(pg.pairwise_corr(df).sort_values(by=['p-unc'])[['X', 'Y', 'n', 'r', 'p-unc']])

print("checkpoint 2")
print(cor)

pingouin_raw_corr = pg.pairwise_corr(df).sort_values(by=['p-unc'])[['X', 'Y', 'n', 'r', 'p-unc']]

pingouin_corr = pd.DataFrame()

for x in df.columns:
    for y in df.columns:
        df[x] = np.nan_to_num(df[x])
        df[y] = np.nan_to_num(df[y])
        print("checkpoint 3 " + str(x) + " " + str(y))
        corr = stats.pearsonr(np.asarray(df[x], dtype="float"), np.asarray(df[y], dtype="float"))
        if (x == y):
            pingouin_corr.loc[x,y] = 1
        else:
            pingouin_corr.loc[x,y] = corr[1]

sns.heatmap(pingouin_corr, annot=True, cmap=plt.cm.Reds)
plt.show()

df.drop(df.index[0])

correlations = {}

for i in range(0, len(labels)):
    label = labels[i]
    cor_target = abs(pingouin_corr[label])
    relevant_features = cor_target[cor_target>0.5] #we're gonna delete all values with correlations above the threshold
    correlations[correlating_labels[i]] = relevant_features
    
#deleting highly correlated values in order to get only one value from each cluster

for l in range(0,len(features)):
    for m in range(l, len(features)):
        if (m >= len(features)):
            continue

        i = correlating_labels[l]
        j = features[m]

        #correlations[i].keys() gives me the names of the correlating features

        print (i)
        print (correlations[i].keys())

        if (np.logical_and(l != m,correlating_labels[m] in correlations[i].keys())):
            features.pop(m)
            m-=1

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

        # class_feature_means = pd.DataFrame(columns=best_features_df.columns)
        # for c, rows in best_features_df.head():
        #     class_feature_means[c] = rows.mean()
        # class_feature_means

        best_features_df_trans = best_features_df.transpose() #transpose to get everything in terms of trial number rather than test

        cluster_labels = clusterer.fit_predict(best_features_df_trans)

        testingNewMeasurements = clusterer.fit_predict(best_features_df_trans)
        labelsOfNewMeasurements = clusterer.labels_

        coefficientsBlock = clusteringscoring.measurements_block(best_features_df_trans.to_numpy(), testingNewMeasurements)

        print("Testing function: " + str(len(coefficientsBlock[0])) + " s " + str(len(coefficientsBlock[1])) + " s " + str(len(coefficientsBlock[2])))
        # Return value of the above function is [intra(A), nearest(b)]

        allDistances = clusterer.fit_transform(best_features_df_trans)
        clusterDistance = allDistances.min(axis=1)
        w = np.mean(clusterDistance)

        centroids = clusterer.cluster_centers_
        
        #1) FInd center of all clusters
        #2) Find distance from each point to the mega-center
        #3) Find Average of those distances
        
        print("centers: " + str(centroids))

        for row in centroids:
            print(str(type(row)) + ", , , , " + str(row.size))

        averageCenterofCenters = [0]*(r+1) #r+1 is the number of features we have
        columnNumber = 0
        for row in centroids:
            for column in np.nditer(row):
                print("col: " + str(columnNumber) + ", " + str(column))
                averageCenterofCenters[columnNumber] += column
                columnNumber+=1
            columnNumber = 0

        counter=0
        for idx in averageCenterofCenters:
            averageCenterofCenters[counter] = idx/n_clusters
            counter+=1

        print("averages: " + str(averageCenterofCenters))
        b=0

        print("checking centers: " + str(centroids))

        for point in centroids:
           print(str(point) + ", " + str(averageCenterofCenters)) 
           tempDist = distance.euclidean(point, averageCenterofCenters) 
           b+=tempDist

        b/=n_clusters

        print("within cluster: " + str(w))
        print("between cluster: " + str(b))


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

best_rep_index = 0
best_rep_coeff = 0

for i in range(0, len(best_features_per_num_of_features)):
    print("_____________________ Best features for " + str(i + 1) + ":  _____________________")
    for x in range(0, len(best_features_per_num_of_features[i])):
        print(best_features_per_num_of_features[i][x].name + " " + str(best_coeff_per_num_of_features[i]))
        if (best_coeff_per_num_of_features[i] > best_rep_coeff):
            best_rep_coeff = best_coeff_per_num_of_features[i]
            best_rep_index = i

best_overall_rep_feature_set = best_features_per_num_of_features[best_rep_index]

print("Best Representative Feature: \n")

for x in range(0, len(best_overall_rep_feature_set)):
    print(best_overall_rep_feature_set[x].name)

print("Best Coefficient: " + str(best_rep_coeff))




# centers, labels = find_clusters(B = features, n_clusters = 2, rseed = 2, iterations = 10)
# features_np = np.array(features)

# plt.scatter(features_np[:, 0], features_np[:, 1], c=labels,
#            s=50, cmap='viridis')
# plt.show()
# #best_coeff_per_num_of_features indicates the silhouette coefficient 

# make sure with professor that our add up algorithm is actually not ass lmao