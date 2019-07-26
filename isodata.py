import numpy as np
from sklearn.metrics import pairwise_distances_argmin
import matplotlib.pyplot as plt

def find_clusters(B, n_clusters, rseed=2, iterations = 10, theta_N = 3):
    # 1. Randomly choose clusters
    X = np.array(B)
    rng = np.random.RandomState(rseed)
    i = rng.permutation(X.shape[0])[:n_clusters]
    centers = X[i]
    cluster_amnt = n_clusters
    # runs the centroid algorithm once.
    for i in range(iterations):
	    # 2a. Assign labels based on closest center
	    labels = pairwise_distances_argmin(X, centers)

	    #labels[i] = index of the particular centroid of the cluster X[i] is within
	    #centers[labels[i]] = cluster id of the cluster that point i is in.

	    # Beginning of the ISODATA program

	    # remove centers that don't have enough elements within them
	    for i in range(cluster_amnt): # iterates through the number of clusters present
	    	freq_i = list(labels.flatten()).count(i)
	    	if freq_i < theta_N: # if we dont satisfy the basic amount of points needed in a cluster
	    		centers.pop(i)
	    		cluster_amnt-=1
	    		labels = pairwise_distances_argmin(X, centers) #re-assigns the cluster centers after removing the center
	    		print ("removed " + str(i) + " to achieve a centroid set of " + str(labels))

	    # compute the average distance between points in clusters and the centers of the clusters

	    # 2b. Find new centers from means of points
	    new_centers = np.array([X[labels == i].mean(0)
	                            for i in range(n_clusters)])
	    # 2c. Check for convergence
	    if np.all(centers == new_centers):
	        print("Breaking due to repeat of centers")
	        break
	    
	    centers = new_centers

	    plt.scatter(X[:, 0], X[:, 1], c=labels, s=50, cmap='viridis')
	    plt.show()
	    input("Press Enter to continue...")
    return centers, labels
#centers, labels = find_clusters(X, 4)

#plt.scatter(X[:, 0], X[:, 1], c=labels,
#           s=50, cmap='viridis');