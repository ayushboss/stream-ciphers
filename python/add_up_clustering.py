import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import csv

data = pd.read_csv('cluster_data.csv', error_bad_lines=False, engine="python") #reads and parses the data

df = pd.DataFrame(data)
columns = list(df)
features = []
for column in df:
	epiclist = df[column]
	features.append(epiclist)

#attempt add up	