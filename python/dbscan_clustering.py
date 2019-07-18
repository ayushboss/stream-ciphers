from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score as silscore
from sklearn.metrics import pairwise_distances as pair_dist
import pandas as pd
import numpy as np
import csv

#reading in and parsing the data
data = pd.read_csv('/tests/cluster_data.csv', error_bad_lines=False, engine="python") 
print(data)

#maybe?? : converting the returned value from read_csv to a nested list to pass into dbscan

#applying dbscan to the data
np_data = np.asarray(data)
print(np_data)

#NEED TO OPTIMIZE THE EPS VALUE IN ORDER TO ENSURE THAT WE GET A GOOD AMOUNT OF CLUSTERSS
#TALK TO DR.TAMIR ABOUT IT

clustering = DBSCAN(eps=0.001, min_samples=2).fit(np_data) 
print(clustering.labels_)
print ("Size of clustering: " + str(len(clustering.labels_)))
print(clustering)

#assess the quality of the clustering scheme by using the sillhouette_score
#this sillhouette score basically tells us about the density of the clustering

overall_clustering_score = silscore(np_data, clustering.labels_, "euclidean")
print(overall_clustering_score)
