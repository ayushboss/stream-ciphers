import numpy as np
from sklearn.metrics import pairwise_distances_argmin
import matplotlib.pyplot as plt

def find_clusters(B, n_clusters, rseed=2, iterations = 10):
    # 1. Randomly choose clusters
    X = np.array(B)
    rng = np.random.RandomState(rseed)
    i = rng.permutation(X.shape[0])[:n_clusters]
    centers = X[i]
    # runs the centroid algorithm once.
    for i in range(iterations):
	    # 2a. Assign labels based on closest center
	    labels = pairwise_distances_argmin(X, centers)

	    # Beginning of the ISODATA program
	    print("center test: " + str(centers))
	    print("WTFAID LABELS: " + str(labels))

	    print(X)

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