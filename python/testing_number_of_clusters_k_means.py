import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import csv

data = pd.read_csv('../cluster_data.csv', error_bad_lines=False, engine="python") #reads and parses the data
print(data)
print(data.head())
print (len(data))
n_clusters = 16

clusterer = KMeans(n_clusters=n_clusters, random_state=10)
cluster_labels = clusterer.fit_predict(data)
silhouette_avg = silhouette_score(data, cluster_labels)
print("Average sillhouette score for cluster size " + str(n_clusters) + " is " + str(silhouette_avg))

