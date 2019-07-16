import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import csv
#add up and knock down
wt = ['wt' + str(i) for i in range(1, 306)]
ko = ['ko' + str(i) for i in range(1, 306)]

s='s'
d = 'd'

z_scaler = StandardScaler()

data = pd.read_csv('cluster_data.csv', error_bad_lines=False, engine="python")
print(data)
print(data.head())

scaled_data = preprocessing.scale(data.T)
pca = PCA()
pca.fit(scaled_data)
pca_data = pca.transform(scaled_data)

per_var = np.round(pca.explained_variance_ratio_ * 100, decimals = 1)
labels = ['PC' + str(x) for x in range(1, len(per_var) + 1)]

plt.bar(x=range(1, len(per_var) + 1), height = per_var, tick_label = labels)
plt.ylabel('Percentage of Expected Variance')
plt.xlabel('Principal Component')
plt.title("Scree Plot")
plt.show()

pca_df = pd.DataFrame(pca_data, index=["Entropy", "Compression"], columns=labels)
plt.scatter(pca_df.PC1, pca_df.PC2)
plt.title("PCA Graph")
plt.xlabel("PCA1 %")
plt.ylabel("PCA2 %")

for sample in pca_df.index:
	plt.annotate(sample, (pca_df.PC1.loc[sample], pca_df.PC2.loc[sample]))

plt.show()

loading_scores = pd.Series(pca.components_[0])
sorted_loading_scores = loading_scores.abs().sort_values(ascending=False)

top_10_contributors = sorted_loading_scores[0:10].index.values

print(loading_scores[top_10_contributors])